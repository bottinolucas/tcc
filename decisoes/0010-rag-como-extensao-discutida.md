# 0010 — Aplicações com LLM entram como extensão discutida

- **Data:** 2026-11-15
- **Status:** substituído por 0013
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

MLOps não se limita a modelos preditivos: aplicações com LLM, como RAG, também precisam de
versionamento, avaliação, promoção e monitoramento. O Gov Hub já tem uma, o **graphrag-tais**
(GraphRAG sobre os metadados do OpenMetadata para responder perguntas e gerar SQL de indicadores),
com dataset gold, baseline aceita e gate (ADR-0012 dele), guardrails (ADR-0016) e mascaramento na
saída (ADR-0018). Era preciso decidir quanto disso entra no TCC.

## Decisão

1. O RAG entra como **extensão discutida**, sem implementação. Título, QP e caso não mudam.
2. Referencial: seção *Aplicações com modelos de linguagem* (RAG, GraphRAG, text-to-SQL, avaliação
   que separa recuperação de geração, LLM como juiz, segurança e LGPD).
3. Proposta: subseção *Extensão para aplicações com modelos de linguagem*, com a tabela papel × caso
   preditivo × aplicação RAG. O papel novo (serviço de inferência online com guardrails) fica **só na
   extensão**, e a tabela de papéis do núcleo não muda.
4. Avaliação: critério qualitativo **AV7**, uma análise de aderência dos papéis ao graphrag-tais.
5. Levar DVC (gold e índice) e MLflow (avaliações, prompts e traces) ao graphrag-tais fica como
   **trabalho futuro**.

## Alternativas consideradas

- **RAG como segundo caso implementado no TCC2:** demonstraria o R8, mas dobra o escopo.
- **Dois casos de mesmo peso:** exigiria reescrever título, QP e objetivos.
- **Só um parágrafo de trabalho futuro:** deixaria sem resposta a pergunta "e LLM?", que a banca
  tende a fazer.

## Consequências

- 13 referências novas no `.bib` (Lewis et al. 2020, Edge et al. 2024, Spider, BIRD, RAGAS, ARES,
  Zheng et al. 2023, Shankar et al. 2024, Greshake et al. 2023, OWASP, graphrag-tais, entre outras).
- A validade externa passa a ter uma evidência qualitativa (AV7), além do R8.
