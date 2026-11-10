# 0006 — Critérios de avaliação AV1–AV5

- **Data:** 2026-11-10
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

A DSR exige que o artefato seja avaliado (ver 0003). Os critérios precisam responder às questões de
pesquisa e usar referências externas, para reduzir o viés de quem também constrói a plataforma.

## Decisão

| ID | Critério | Procedimento | Questão |
|---|---|---|---|
| AV1 | Aderência aos princípios de MLOps | Para cada princípio P1–P9 de Kreuzberger et al. (2023), indicar o componente que o atende ou justificar por que não atende | QP, QE1 |
| AV2 | Prontidão para produção | Aplicar o ML Test Score (Breck et al., 2017) antes e depois da implementação | QP |
| AV3 | Reprodutibilidade | Refazer o treino em ambiente limpo a partir do commit e da versão do dataset, e comparar métricas e predições | QE2 |
| AV4 | Ausência de vazamento temporal | Testes no dbt garantem que nenhuma feature do mês t usa dado posterior a t e que os cortes respeitam a ordem temporal | QE3 |
| AV5 | Comparação com a regra vigente | recall@k e precision@k do modelo e da regra no período de teste | QE3 |

## Alternativas consideradas

- **Avaliar só o desempenho do modelo:** é incompatível com a decisão 0002.
- **Avaliação qualitativa com a equipe técnica:** ainda está em aberto e depende dos orientadores.

## Consequências

- AV3 e AV4 exigem que o manifesto do dataset e os testes de vazamento sejam implementados desde o
  início do TCC2.
- AV2 exige uma aplicação "antes" do ML Test Score, que pode ser feita já, sobre o estado atual da
  plataforma.
