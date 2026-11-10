# 0002 — Contribuição central: a arquitetura, validada por um caso

- **Data:** 2026-11-10
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

O trabalho tem dois produtos possíveis: a arquitetura de MLOps e o modelo preditivo de paralisação
de obras. Era preciso definir qual dos dois é a contribuição, porque isso muda o título, o
referencial e, principalmente, como o trabalho é avaliado.

## Decisão

A contribuição central é **a arquitetura de MLOps**. A previsão de paralisação de obras do MCMV é o
caso que instancia e valida a arquitetura.

A ideia central da arquitetura é **estender a plataforma existente em vez de construir uma
plataforma de ML paralela**:

- features, rótulo e monitoramento ficam no dbt;
- o Python só treina, avalia e escora;
- o Airflow orquestra;
- cada treino congela um dataset versionado no lake.

## Alternativas consideradas

- **Contribuição centrada no modelo preditivo:** exigiria mudar o título, e o resultado do TCC
  ficaria refém do desempenho do modelo.
- **Peso igual para arquitetura e modelo:** dispersaria o trabalho entre duas avaliações completas
  em um único semestre de TCC2.

## Consequências

- Se o modelo não superar a regra vigente, o trabalho continua válido, desde que a comparação tenha
  sido feita de forma correta e reprodutível. Isso está escrito na seção 3.4 do texto.
- A avaliação principal é sobre a arquitetura (AV1–AV4). O desempenho do modelo é avaliado só pelo
  AV5 (ver 0006).
