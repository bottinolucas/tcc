# 0012 — Requisito de equidade (R9) e critério AV6

- **Data:** 2026-11-15
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

O escore decide para onde vai a fiscalização. Um modelo com bom recall@k agregado pode concentrar
as visitas em algumas regiões ou modalidades e deixar outras descobertas. No setor público, isso é
um risco de política pública, e não só de qualidade do modelo (Mehrabi et al., 2022).

## Decisão

1. Novo requisito **R9**: o desempenho dos escores é calculado e monitorado também por subgrupo
   (UF, região, modalidade), e não só no agregado. O cálculo fica na camada de transformação, junto
   com o restante do monitoramento.
2. Novo critério **AV6**: recall@k do modelo e da regra vigente por subgrupo, e a diferença entre o
   melhor e o pior subgrupo. A pergunta é se o modelo reduz ou amplia a desigualdade de cobertura que
   já existe na regra.
3. O model card traz o desempenho por subgrupo (Mitchell et al., 2019).

## Alternativas consideradas

- **Só no model card, sem virar requisito:** a equidade ficaria como propriedade do modelo, e não
  como algo que a arquitetura garante continuamente.
- **Fora do escopo:** deixaria uma pergunta óbvia da banca sem resposta.

## Consequências

- A tabela de requisitos passa a ter R1–R9, e a de avaliação AV1–AV7 (o AV7 vem da decisão 0010).
- A2 (regra vigente) passa a ser calculada também por subgrupo.
