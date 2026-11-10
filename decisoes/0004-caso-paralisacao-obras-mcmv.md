# 0004 — Caso: prevenção de paralisação de obras do MCMV

- **Data:** 2026-11-10
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

A arquitetura precisa de um caso real para ser demonstrada (ver 0002). No Gov Hub Cidades, a
identificação de obras em risco usa hoje uma regra fixa
(`ouro_reloginho_indicadores_gargalo_desempenho`): 90 dias sem atualização, diferença
físico-financeira acima de 10 p.p. ou menos de 30% de execução. Essa regra nunca foi comparada com
as paralisações que de fato aconteceram.

## Decisão

O caso é **prever quais obras ativas do MCMV vão paralisar até o mês t + h**. A saída é um ranking
mensal de risco para priorizar a fiscalização.

- **Unidade:** a obra (`id_empreendimento`) em um mês de competência.
- **Escopo:** FAR, FDS, Rural, Pró-Moradia e Financiado (FGTS). Ficam de fora as modalidades sem
  execução de obra.
- **Referência de comparação:** a regra de gargalo vigente.
- **Métrica principal:** recall@k, com k igual à capacidade mensal de fiscalização.
- **Fonte de verdade:** `data-application-cidades/docs/adr/0001-arquitetura-mlops-prevencao-paralisacao.md`
  e `ml/prevencao_paralisacao/README.md`.

## Alternativas consideradas

- **Outro modelo ou outro órgão do Gov Hub:** nenhum outro tem histórico tão longo, já preparado
  nas camadas prata (dez/2019 a jul/2026), nem uma regra vigente para servir de comparação.

## Consequências

- O levantamento de 27/10/2026 mostrou que a fonte da situação muda duas vezes ao longo da série.
  O rótulo só é confiável no período SFTP (até nov/2024). Isso entra nas ameaças à validade.
- Ainda dependem do MCID: o horizonte h, a capacidade k, a regra de retomada e o usuário do alerta.
  Elas estão em "Decisões em aberto" no `README.md`.
