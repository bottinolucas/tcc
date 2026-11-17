# 0013 — Aplicações com LLM entram só como discussão textual

- **Data:** 2026-11-16
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

A decisão 0010 trouxe as aplicações com LLM como extensão discutida, com uma tabela papel × caso
preditivo × RAG e um critério qualitativo (AV7) sobre o graphrag-tais. O parecer do TCC1
(16/11/2026) apontou que a extensão ocupava quatro pontos do texto (2.4, 4.2.7, AV7 e resumo) sem
estar na pergunta nem nos objetivos. Apontou também que a evidência prevista (análise dos autores
sobre um sistema do próprio laboratório) mostra aderência, e não generalização. A dupla decidiu que
a contribuição é a arquitetura validada pelo caso preditivo, e que o LLM entra apenas para dizer que
a arquitetura também comporta produtos mais novos, como o RAG.

## Decisão

1. A Seção 4.2.7 da Proposta vira uma subseção curta (2 ou 3 parágrafos), **sem tabela e sem
   critério de avaliação**. Ela diz que os papéis comportam aplicações RAG, aponta o análogo do R1
   (nenhum documento do índice fora do catálogo) e o papel adicional (serviço de inferência com
   guardrails).
2. A Seção 2.4 do Referencial encolhe para um ou dois parágrafos.
3. O critério AV7 (aderência ao graphrag-tais) sai. O identificador AV7 passa a ser a
   rastreabilidade (ver 0016).
4. Levar o graphrag-tais para a mesma pilha (DVC, MLflow) continua como trabalho futuro.

## Alternativas consideradas

- **Manter a tabela como ilustração:** ocupa espaço e convida a banca a cobrar uma avaliação.
- **Só um parágrafo de trabalho futuro:** deixa sem resposta a pergunta "e LLM?".

## Consequências

- Substitui a 0010.
- Pergunta, objetivos e resumo não falam em LLM, exceto por uma frase no resumo.
- As referências de LLM que ficarem sem citação saem do `.bib`.
