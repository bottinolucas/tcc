# 0009 — Stack de MLOps da instanciação

- **Data:** 2026-11-15
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

As ferramentas de MLOps apareciam no texto só de passagem. O DVC já estava na tabela de papéis, na
reprodutibilidade e no AV3, mas sem base teórica, sem lugar no repositório e fora da figura da
arquitetura. O MLflow era descrito com "estágios", que a própria ferramenta deixou de recomendar.
Faltava também dizer qual nível de maturidade a arquitetura busca e por que alguns componentes
comuns em MLOps (feature store, serving online) ficam de fora.

## Decisão

1. **Maturidade-alvo: nível 1 do Google** (treino contínuo automatizado). O ciclo export → escore →
   retreino → gate é disparado quando a ouro de uma nova competência é materializada (Assets do
   Airflow 3). O nível 2 fica fora: o custo não se justifica num escore mensal em lote.
2. **DVC para os datasets congelados.** Configuração em `.dvc/` na raiz do `data-application-cidades`,
   remoto `s3://data-lake-mcid/ml/datasets/` e estágio de export em `ml/<modelo>/dvc.yaml` +
   `dvc.lock`. O hash do DVC substitui a parte do manifesto que identificava o conteúdo.
3. **MLflow com apelidos** `champion` (vigente) e `challenger` (candidata). O gate (R5) promove
   movendo o apelido, e o rollback move de volta. Cada execução registra o commit, o hash DVC, a
   versão do dbt, o `uv.lock` e as sementes. Model card e datasheet entram como artefatos.
4. **Validação em três pontos:** testes do dbt (inclusive de vazamento), contratos ODCS das fontes
   (`contracts/`) e Pandera na leitura do dataset pelo Python.
5. **Sem feature store dedicado.** A ouro *as of t* já garante correção na data, e não há inferência
   online. Um Feast seria uma segunda implementação das features, o que contraria o R1.
6. **Monitoramento em dois tempos:** PSI por feature logo após o escore (sinal antecipado) e
   desempenho realizado quando o rótulo chega, h meses depois. O retreino é periódico e é
   antecipado por alerta de PSI.
7. **CI no PR:** lint, `dbt build` com testes e um treino de fumaça com amostra, com as métricas
   comentadas no PR.

## Alternativas consideradas

- **lakeFS ou time travel do Iceberg/Delta no lugar do DVC:** dependem de um formato de tabela
  aberto que o motor (PostgreSQL + pg_duckdb) não usa.
- **Feast como feature store:** só traria vantagem com inferência online.
- **Evidently ou estimativa de desempenho sem rótulo (NannyML):** acrescentam componente e tiram parte
  do cálculo do dbt. Ficam como opção se o PSI não bastar.
- **Nível 2 de maturidade:** o custo é desproporcional ao caso.

## Consequências

- Referencial: novas subseções de versionamento de dados e de maturidade-alvo; MLflow com apelidos;
  validação (Schelter et al., 2018), atraso do rótulo (Lu et al., 2019) e reprodutibilidade (Pineau
  et al., 2021).
- Proposta: figura com o papel de versionamento de dados, parágrafos sobre feature store,
  validação, CI, promoção e monitoramento; tabela de ferramentas com o local do DVC.
- A decisão em aberto "Limiares de alerta de drift e política de retreino" passa a ter uma proposta
  concreta; só os valores de PSI seguem em aberto, a calibrar na EDA.
