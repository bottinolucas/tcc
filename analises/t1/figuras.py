"""Gera o código pgfplots das figuras da sprint T1 (perguntas 1 e 2 da EDA) a partir dos CSVs de analises/t1/saida/.
Uso: python analises/t1/figuras.py  (grava figuras/t1_obras_por_fonte.tex e figuras/t1_taxa_paralisacao.tex)"""
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).parent
FIG = AQUI.parent.parent / "figuras"
MODALIDADES = [("FAR", "FAR"), ("FDS", "FDS"), ("RURAL", "Rural")]
FONTES = [("SFTP", "blue!70!black", "solid"), ("SNH", "orange!90!black", "solid"), ("Planilha mensal", "green!50!black", "solid")]
TROCAS = ["06/2024", "08/2024", "09/2024", "04/2026"]
TROCA_SO_FDS = "06/2026"  # o FDS inteiro volta a vir do SFTP nesse mês
MIN_EM_OBRAS = 30  # taxa só em mês com 30 obras ou mais em execução no mês anterior
TICKS = ["12/2019", "12/2020", "12/2021", "12/2022", "12/2023", "06/2024", "12/2024", "12/2025", "07/2026"]


def idx(c):
    m, a = c.split("/")
    return (int(a) - 2019) * 12 + int(m) - 12


def serie(df, mod, fonte, valor):
    """Valor por mês entre o primeiro e o último mês da fonte; 0 se a modalidade tem dado no mês e a fonte não; nan (linha quebrada) se não há dado."""
    m = df[df.modalidade == mod]
    s = m[m.fonte == fonte].set_index("i")[valor]
    if s.empty:
        return s
    meses = range(s.index.min(), s.index.max() + 1)
    com_dado = set(m.i)
    return s.reindex(meses).where(lambda x: x.notna() | ~x.index.isin(com_dado), 0.0) if valor == "n_obras" else s.reindex(meses)


def figura(df, valor, ylabel, fontes, legenda):
    linhas = [
        "% Gerado por analises/t1/figuras.py a partir de analises/t1/saida/. Não editar à mão.",
        "\\begin{tikzpicture}",
        "\\begin{groupplot}[group style={group size=1 by 3, vertical sep=0.55cm, xticklabels at=edge bottom},",
        "  width=\\textwidth, height=3.9cm, xmin=0, xmax=79, ymin=0, grid=major, grid style={gray!20}, unbounded coords=jump,",
        f"  xtick={{{','.join(str(idx(t)) for t in TICKS)}}}, xticklabels={{{','.join(TICKS)}}},",
        "  x tick label style={rotate=45, anchor=north east, font=\\scriptsize}, y tick label style={font=\\scriptsize},",
        "  /pgf/number format/use comma, /pgf/number format/1000 sep={.}]",
    ]
    for i, (mod, nome) in enumerate(MODALIDADES):
        extra = f", legend to name=leg{valor}, legend columns={len(fontes)}, legend style={{font=\\footnotesize, draw=none}}" if i == 0 else ""
        linhas.append(f"\\nextgroupplot[ylabel={{{ylabel}}}, ylabel style={{font=\\scriptsize}}, title={{{nome}}}, title style={{font=\\footnotesize, yshift=-1.5ex}}{extra}]")
        for fonte, cor, estilo in fontes:
            s = serie(df, mod, fonte, valor)
            if s.empty:
                linhas.append(f"\\addlegendimage{{{cor}, thick}}\\addlegendentry{{{fonte}}}" if i == 0 else "")
                continue
            pts = " ".join(f"({i},{v:.4f})" if v == v else f"({i},nan)" for i, v in s.items())
            linhas.append(f"\\addplot[{cor}, thick, mark=none] coordinates {{{pts}}};")
            if i == 0:
                linhas.append(f"\\addlegendentry{{{fonte}}}")
        for c in TROCAS + ([TROCA_SO_FDS] if mod == "FDS" else []):
            linhas.append(f"\\draw[gray!70, dashed] ({{axis cs:{idx(c)},0}}|-{{rel axis cs:0,0}}) -- ({{axis cs:{idx(c)},0}}|-{{rel axis cs:0,1}});")
    linhas += ["\\end{groupplot}", f"\\node[anchor=north] at ($(group c1r3.south)+(0,-1.25cm)$) {{\\pgfplotslegendfromname{{leg{valor}}}}};", "\\end{tikzpicture}"]
    return "\n".join(l for l in linhas if l)


n = pd.read_csv(AQUI / "saida" / "b3_obras_por_mes_e_fonte.csv")
n["i"] = n.competencia.map(idx)
(FIG / "t1_obras_por_fonte.tex").write_text(figura(n, "n_obras", "obras no mês", FONTES, True), encoding="utf-8")
t = pd.read_csv(AQUI / "saida" / "b3_taxa_paralisacao.csv")
t["i"] = t.competencia.map(idx)
t["pct"] = (100 * t.taxa).where(t.em_obras_mes_anterior >= MIN_EM_OBRAS)
(FIG / "t1_taxa_paralisacao.tex").write_text(figura(t, "pct", "\\% que paralisa", FONTES[:2], True), encoding="utf-8")
print("ok", sorted(p.name for p in FIG.glob("t1_*.tex")))
