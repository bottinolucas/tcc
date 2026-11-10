# 0001 — Tema: arquitetura de MLOps para dados governamentais

- **Data:** 2026-11-10
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

O trabalho é feito no LabLivre (Laboratório de Competência em Software Livre, UnB), dentro do projeto Gov Hub, que constrói plataformas de dados
para órgãos federais. A plataforma do Ministério das Cidades (Gov Hub Cidades) já tem ingestão com
Airflow, transformação em camadas com dbt, data lake, Superset e catálogo no OpenMetadata, mas
nenhum componente de aprendizado de máquina.

Em outubro de 2026, o ADR 0001 do repositório `data-application-cidades` propôs uma arquitetura de
MLOps para prever a paralisação de obras. Em 09/11/2026 o título do documento no Overleaf mudou
para "Arquitetura de MLOps para dados governamentais".

## Decisão

O tema do TCC é **a arquitetura de MLOps para plataformas de dados governamentais**, com o título
"Arquitetura de MLOps para dados governamentais".

## Alternativas consideradas

- **Integração semântica de bases governamentais com LLM** (repositório
  `Integracao-de-Dados-com-Modelos-de-Linguagem`): essa linha seguiu como artigo próprio (CAIN 2027)
  e não faz parte deste TCC.
- **Arquitetura de engenharia de dados config-driven** (PoC `poc-arquitetura-govhub`): foi
  descartada como tema central porque a plataforma já tem essas práticas. Ela entra apenas como
  contexto no referencial (seção 2.1).

## Consequências

- O referencial teórico se concentra em sistemas de ML em produção e em MLOps. Engenharia de dados
  aparece só como base.
- O trabalho depende do acesso ao repositório e aos dados do Gov Hub Cidades.
