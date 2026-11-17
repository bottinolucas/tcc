"""Sprint T1 do TCC1: números do Capítulo 4.3.1 e do Capítulo 5 a partir da plataforma Gov Hub Cidades.

Lê as tabelas prata de histórico do FAR, do FDS e do Rural (banco de homologação) e a silver da
série histórica (prata_dhist_*). Grava os CSVs em analises/t1/saida/ e imprime as tabelas.

Conexões, por variáveis de ambiente (só leitura):
  PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE   banco de homologação (painel histórico)
  DHIST_URL   banco onde está a silver prata_dhist_* (até o merge, o banco local de validação)
Uso: python analises/t1/t1.py
"""
import os
from pathlib import Path

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

SAIDA = Path(__file__).parent / "saida"
SAIDA.mkdir(exist_ok=True)
HOM = create_engine(
    f"postgresql+psycopg2://{os.environ['PGUSER']}:{os.environ['PGPASSWORD']}@{os.environ['PGHOST']}:{os.environ.get('PGPORT', '5432')}/{os.environ['PGDATABASE']}",
    connect_args={"connect_timeout": 30, "options": "-c default_transaction_read_only=on"},
)
DHIST = create_engine(os.environ["DHIST_URL"])
MODALIDADES = ("far", "fds", "rural")
FONTE = {"sftp": "SFTP", "snh": "SNH", "obra_mensal": "Planilha mensal"}
TROCA = pd.Timestamp("2024-06-01")          # primeira competência em que a situação passa a vir da SNH
IDA_E_VOLTA = pd.to_datetime(["2024-06-01", "2024-08-01", "2024-09-01"])


def sql(engine, q):
    with engine.connect() as c:
        return pd.read_sql(text(q), c)


# ---------------------------------------------------------------- extração
SQL_PAINEL = """
select '{m}' as modalidade, coalesce(id_empreendimento, apf) as obra, ltrim(apf, '0') as apf,
       date_trunc('month', dt_referencia)::date as mes, fonte_serie, fonte_valor, situacao_canonica as sit,
       percentual_execucao_fisica as fis, percentual_execucao_financeira as fin, valor_contratado as vc,
       valor_desembolsado as vd, dt_contratacao, dt_previsao_entrega, pc_obra_prevista, dt_inicio_obra,
       dt_conclusao_obra, dt_entrega_uh, dt_primeira_entrega, dt_ultima_liberacao
from prata.prata_hist_{m}_empreendimento
where dt_referencia between '2019-12-01' and '2026-07-31'
"""
SQL_PREVISAO_SERIE_HISTORICA = """
select ltrim(apf, '0') as apf, competencia, max(dt_previsao_termino_obra) as prev
from prata.prata_dhist_relatorio_executivo_caixa
where produto in ('FAR Alienação', 'FDS') and apf is not null and dt_previsao_termino_obra is not null
group by 1, 2
"""
SQL_PREVISAO_ATUAL = """
select ltrim(apf, '0') as apf, dt_previsao_entrega as prev from prata.prata_far_dados_prioritarios_caixa where dt_previsao_entrega is not null
union all
select ltrim(apf, '0'), dt_previsao_entrega from prata.prata_fds_empreendimento where dt_previsao_entrega is not null
"""
SQL_CODIGOS_PLANILHA = """
select '{m}' as modalidade, co_situacao_obra::text as cod, count(*) as n
from prata.prata_hist_{m}_empreendimento where fonte_serie = 'obra_mensal' group by 1, 2
"""


def painel():
    p = pd.concat([sql(HOM, SQL_PAINEL.format(m=m)) for m in MODALIDADES]).reset_index(drop=True)
    p["modalidade"] = p.modalidade.str.upper()
    for c in [c for c in p.columns if c.startswith("dt_")] + ["mes"]:
        p[c] = pd.to_datetime(p[c], errors="coerce")
    for c in ("fis", "fin", "vc", "vd", "pc_obra_prevista"):
        p[c] = pd.to_numeric(p[c], errors="coerce")
    return p


def uma_linha_por_obra_e_mes(p, so_com_situacao=True):
    """No FDS a obra (id_empreendimento) pode ter mais de um APF no mês: vale a SNH, depois o SFTP, depois a planilha."""
    q = p[p.sit.notna()] if so_com_situacao else p
    q = q.assign(_pri=q.fonte_serie.map({"snh": 0, "sftp": 1, "obra_mensal": 2}))
    q = q.sort_values(["modalidade", "obra", "mes", "_pri", "apf"]).drop_duplicates(["modalidade", "obra", "mes"]).reset_index(drop=True)
    g = q.groupby(["modalidade", "obra"])
    q["sit_ant"], q["fonte_ant"] = g.sit.shift(), g.fonte_serie.shift()
    return q


# ---------------------------------------------------------------- bloco 1
def bloco1(p):
    obras = p.groupby("modalidade").agg(apfs=("apf", "nunique"), obras=("obra", "nunique"))
    obras.loc["Total"] = obras.sum()
    q = uma_linha_por_obra_e_mes(p)
    fontes_mes = q[q.mes.between("2024-04-01", "2025-01-01")].pivot_table(index=["modalidade", "mes"], columns="fonte_serie", values="obra", aggfunc="size", fill_value=0)
    t = q[(q.sit_ant == "em_obras") & (q.sit == "paralisada")].copy()
    t["periodo"] = np.select([t.mes < TROCA, t.mes == TROCA], ["a_sftp_antes", "b_mes_da_troca"], "c_snh_depois")
    t["primeira"] = ~t.duplicated(["modalidade", "obra"])
    t["mudou_fonte"] = t.fonte_ant != t.fonte_serie

    def tabela(x):
        r = x.pivot_table(index="modalidade", columns="periodo", values="obra", aggfunc="size", fill_value=0)
        r.loc["Total"] = r.sum()
        r["total"] = r.sum(axis=1)
        return r

    todas, primeiras = tabela(t), tabela(t[t.primeira])
    mudanca = t.groupby("modalidade").mudou_fonte.sum()
    obras.to_csv(SAIDA / "b1_obras.csv")
    todas.to_csv(SAIDA / "b1_transicoes_todas.csv")
    primeiras.to_csv(SAIDA / "b1_transicoes_primeira_paralisacao.csv")
    fontes_mes.to_csv(SAIDA / "b1_obras_por_fonte_2024.csv")
    return obras, fontes_mes, todas, primeiras, mudanca, t


# ---------------------------------------------------------------- bloco 2
def bloco2(p):
    d = uma_linha_por_obra_e_mes(p[p.modalidade.isin(["FAR", "FDS"])])
    g = d.groupby(["modalidade", "obra"])
    d["fim_mes"] = d.mes + pd.offsets.MonthEnd(0)
    # o que a regra usa, só com o que se sabia até t
    d["lib_derivada"] = d.mes.where(g.vd.diff() > 0).groupby([d.modalidade, d.obra]).ffill()
    d["med_derivada"] = d.mes.where(g.fis.diff().fillna(1) != 0).groupby([d.modalidade, d.obra]).ffill().where(d.modalidade == "FAR")

    def ate_t(c):
        return d[c].where(d[c] <= d.fim_mes)

    d["lib_t"] = pd.to_datetime(np.where(d.modalidade == "FAR", ate_t("dt_ultima_liberacao").fillna(d.lib_derivada), d.lib_derivada))
    d["entrega_t"] = pd.to_datetime(np.where(d.modalidade == "FAR", ate_t("dt_primeira_entrega"), ate_t("dt_entrega_uh")))
    d["conclusao_t"] = ate_t("dt_conclusao_obra")
    d["inicio_t"] = ate_t("dt_inicio_obra").where(d.modalidade == "FDS")
    d["dt_ultima_atualizacao"] = d[["lib_t", "med_derivada", "entrega_t", "conclusao_t", "dt_contratacao", "inicio_t"]].max(axis=1)
    # previsão de conclusão: o painel não guarda (0% das linhas no SFTP); vale o último valor conhecido até t
    # (relatório executivo, até 08/2018) e, na falta, o primeiro registrado depois de t
    rel = sql(DHIST, SQL_PREVISAO_SERIE_HISTORICA)
    rel["prev"], rel["competencia"] = pd.to_datetime(rel.prev), pd.to_datetime(rel.competencia)
    atual = sql(HOM, SQL_PREVISAO_ATUAL).assign(prev=lambda x: pd.to_datetime(x.prev)).groupby("apf").prev.first()
    no_painel = d.dropna(subset=["dt_previsao_entrega"]).sort_values("mes").groupby("apf").dt_previsao_entrega.first()
    d["prev_passado"] = d.apf.map(rel.sort_values("competencia").groupby("apf").prev.last())
    d["prev_posterior"] = d.apf.map(no_painel).fillna(d.apf.map(atual))
    d["prev_origem"] = np.select([d.prev_passado.notna(), d.prev_posterior.notna()], ["vigente até t", "primeiro valor registrado depois de t"], "sem previsão")
    trans = d[(d.sit_ant == "em_obras") & (d.sit == "paralisada")][["modalidade", "obra", "mes"]]

    def rodar(prev, excluir, fracs=(0.05, 0.10, 0.20)):
        ev = trans[~trans.mes.isin(excluir)].groupby(["modalidade", "obra"]).mes.min().rename("mes_evento")
        x = d.join(ev, on=["modalidade", "obra"])
        x = x[(x.sit == "em_obras") & (x.mes_evento.isna() | (x.mes_evento > x.mes)) & x.mes.between("2019-12-01", "2024-05-01")].copy()
        t_, pv = x.fim_mes, (x[prev] if prev else pd.Series(pd.NaT, index=x.index))
        fis, fin = x.fis.fillna(0), x.fin.fillna(0)
        x["dias_atraso"] = np.where(pv.notna() & (pv < t_) & (fis < 100), (t_ - pv).dt.days, 0)
        x["dias_sem_atualizacao"] = (t_ - x.dt_ultima_atualizacao).dt.days
        saldo = np.where(x.vc.fillna(0) > 0, (x.vc.fillna(0) - x.vd.fillna(0)).clip(lower=0) / x.vc * 100, 0)
        ano = t_ - pd.Timedelta(days=365)
        x["score"] = (
            2 * (x.dias_atraso > 0)
            + (x.dt_ultima_atualizacao.isna() | (x.dias_sem_atualizacao > 90))
            + ((fis < 100) & ((fis < x.pc_obra_prevista.fillna(fis) - 10) | (pv.notna() & (pv < t_)) | ((x.dt_contratacao < ano) & (fis < 30))))
            + ((fin < np.maximum(fis - 10, 0)) | ((x.dt_contratacao < ano) & (fin < 30)))
            + ((x.vc.fillna(0) > 0) & (saldo >= 30) & (fis < 95))
            + ((x.dt_contratacao < t_ - pd.Timedelta(days=180)) & (fis == 0) & (fin == 0))
        )
        x["evento"] = x.mes_evento.notna() & (x.mes_evento <= x.mes + pd.DateOffset(months=6))
        x["_sem"] = x.dias_sem_atualizacao.fillna(10**6)
        x = x.sort_values(["modalidade", "mes", "score", "_sem", "dias_atraso", "apf"], ascending=[True, True, False, False, False, True])
        x["pos"] = x.groupby(["modalidade", "mes"]).cumcount() + 1
        x["n"] = x.groupby(["modalidade", "mes"]).obra.transform("size")
        linhas = []
        for mod, m in x.groupby("modalidade"):
            r = {"modalidade": mod, "competencias": m.mes.nunique(), "obra_mes_em_risco": len(m), "eventos": int(m.evento.sum()),
                 "obras_com_evento": m[m.evento].obra.nunique(), "taxa_base": m.evento.mean()}
            for f in fracs:
                top = m.pos <= np.ceil(f * m.n)
                ac, ev_, kk = (top & m.evento).groupby(m.mes).sum(), m.evento.groupby(m.mes).sum(), top.groupby(m.mes).sum()
                r[f"recall_{int(f * 100)}_total"] = ac.sum() / ev_.sum()
                r[f"recall_{int(f * 100)}_media"] = (ac[ev_ > 0] / ev_[ev_ > 0]).mean()
                r[f"precision_{int(f * 100)}_total"] = ac.sum() / kk.sum()
            linhas.append(r)
        return pd.DataFrame(linhas).set_index("modalidade"), x

    d["prev_mix"] = d.prev_passado.fillna(d.prev_posterior)
    variantes = {"principal": ("prev_mix", [TROCA]), "so_previsao_ate_t": ("prev_passado", [TROCA]),
                 "sem_previsao": (None, [TROCA]), "principal_sem_06_08_09_2024": ("prev_mix", IDA_E_VOLTA)}
    res = {}
    for nome, (prev, excl) in variantes.items():
        res[nome], x = rodar(prev, excl)
        res[nome].to_csv(SAIDA / f"b2_regra_{nome}.csv")
        if nome == "principal":
            origem = x.drop_duplicates(["modalidade", "obra"]).groupby(["modalidade", "prev_origem"]).size().unstack(fill_value=0)
            origem.to_csv(SAIDA / "b2_origem_previsao.csv")
            concl = x[x.evento].groupby("modalidade").size()
    return res, origem


# ---------------------------------------------------------------- bloco 3
def bloco3(p):
    todas = uma_linha_por_obra_e_mes(p, so_com_situacao=False)
    n = todas.assign(fonte=todas.fonte_serie.map(FONTE)).groupby(["mes", "fonte", "modalidade"]).obra.nunique().rename("n_obras").reset_index()
    n.insert(0, "competencia", n.mes.dt.strftime("%m/%Y"))
    n.drop(columns="mes").to_csv(SAIDA / "b3_obras_por_mes_e_fonte.csv", index=False)
    q = uma_linha_por_obra_e_mes(p)
    b = q[q.sit_ant == "em_obras"].assign(fonte=lambda x: x.fonte_serie.map(FONTE))
    taxa = b.groupby(["mes", "fonte", "modalidade"]).agg(transicoes=("sit", lambda s: int((s == "paralisada").sum())), em_obras_mes_anterior=("obra", "size")).reset_index()
    taxa["taxa"] = taxa.transicoes / taxa.em_obras_mes_anterior
    taxa.insert(0, "competencia", taxa.mes.dt.strftime("%m/%Y"))
    taxa.drop(columns="mes")[["competencia", "fonte", "modalidade", "taxa", "transicoes", "em_obras_mes_anterior"]].to_csv(SAIDA / "b3_taxa_paralisacao.csv", index=False)
    planilha = pd.concat([sql(HOM, SQL_CODIGOS_PLANILHA.format(m=m)) for m in MODALIDADES])
    dic_far = sql(HOM, "select co_situacao_obra::text as cod, situacao_obra as descricao from seeds.far_situacao_obra")
    dic_rur = sql(HOM, "select codigo::text as cod, descricao, estagio from seeds.dominio_rural_obra where campo = 'co_situacao_operacao'")
    dominio = sql(HOM, "select lower(valor_bruto) as k, situacao_canonica from seeds.dominio_status")
    import unicodedata

    def k(s):
        return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().strip().lower()

    dom = {k(a): b for a, b in zip(dominio.k, dominio.situacao_canonica)}
    pl = planilha.pivot_table(index="cod", columns="modalidade", values="n", fill_value=0).reset_index()
    pl = pl.merge(dic_far.rename(columns={"descricao": "descricao_far_fds"}), on="cod", how="left").merge(dic_rur.rename(columns={"descricao": "descricao_rural"}), on="cod", how="left")
    pl["situacao_canonica"] = pl.descricao_far_fds.map(lambda s: dom.get(k(s)))
    pl.to_csv(SAIDA / "b3_depara_planilha_mensal.csv", index=False)
    fg = sql(HOM, "select cod_situacao_obra as cod, situacao_obra as descricao, count(*) as n from prata.prata_financiado_obra_mensal group by 1, 2 order by 1")
    fg["situacao_canonica"] = fg.descricao.map(lambda s: dom.get(k(s)) if s else None)
    fg.to_csv(SAIDA / "b3_depara_fgts.csv", index=False)
    return n, taxa, pl, fg


# ---------------------------------------------------------------- bloco 4
def bloco4(p):
    d = uma_linha_por_obra_e_mes(p)[["modalidade", "obra", "mes", "sit", "sit_ant"]]
    tr = d[(d.sit_ant == "em_obras") & (d.sit == "paralisada") & (d.mes != TROCA)]
    ev = tr.groupby(["modalidade", "obra"]).mes.min().rename("mes_evento")
    x = d.join(ev, on=["modalidade", "obra"])
    base = x[(x.sit == "em_obras") & (x.mes_evento.isna() | (x.mes_evento > x.mes)) & x.mes.between("2019-12-01", "2024-05-01")][["modalidade", "obra", "mes"]]
    look = d.set_index(["modalidade", "obra", "mes"]).sit
    vivo = pd.Series(True, index=base.index)
    linhas = pd.Series(0, index=sorted(base.modalidade.unique()))
    eventos = linhas.copy()
    for j in range(1, 7):
        alvo_mes = base.mes + pd.DateOffset(months=j)
        sj = pd.Series(look.reindex(pd.MultiIndex.from_arrays([base.modalidade, base.obra, alvo_mes])).values, index=base.index)
        obs = vivo & sj.notna()
        y = obs & sj.eq("paralisada") & (alvo_mes != TROCA)
        linhas += obs.groupby(base.modalidade).sum()
        eventos += y.groupby(base.modalidade).sum()
        vivo = obs & sj.isin(["em_obras", "nao_iniciada"]) & ~y
    r = pd.DataFrame({"pares_obra_t": base.groupby("modalidade").size(), "linhas_obra_t_j": linhas, "linhas_com_evento": eventos})
    r.loc["Total"] = r.sum()
    r.to_csv(SAIDA / "b4_linhas_marco.csv")
    q = p[p.modalidade.isin(["FAR", "FDS"])]
    atrasos = []
    for c in ("dt_inicio_obra", "dt_conclusao_obra", "dt_primeira_entrega", "dt_entrega_uh", "dt_ultima_liberacao"):
        z = q[["modalidade", "obra", "mes", c]].dropna()
        z = z[z[c] >= "2020-01-01"]
        f = z.sort_values("mes").groupby(["modalidade", "obra", c]).mes.min().reset_index()
        f["atraso"] = (f.mes.dt.year - f[c].dt.year) * 12 + (f.mes.dt.month - f[c].dt.month)
        for mod, gg in f.groupby("modalidade"):
            atrasos.append({"data": c, "modalidade": mod, "valores": len(gg), "mediana_meses": gg.atraso.median(),
                            "pct_mais_de_1_mes": 100 * (gg.atraso > 1).mean(), "pct_mais_de_3_meses": 100 * (gg.atraso > 3).mean(),
                            "pct_data_depois_do_mes": 100 * (gg.atraso < 0).mean()})
    atrasos = pd.DataFrame(atrasos)
    atrasos.to_csv(SAIDA / "b4_atraso_de_registro.csv", index=False)
    return r, atrasos


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    print("extração:", pd.Timestamp.today().strftime("%d/%m/%Y"))
    p = painel()
    for nome, saida in [("BLOCO 1", bloco1(p)[:5]), ("BLOCO 2", bloco2(p)), ("BLOCO 3", bloco3(p)[2:]), ("BLOCO 4", bloco4(p))]:
        print(f"\n######## {nome}")
        for s in saida:
            print(s.to_string() if hasattr(s, "to_string") else s, "\n")
