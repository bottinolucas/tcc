# 0005 — Escopo e estrutura do documento do TCC1

- **Data:** 2026-11-10
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

O documento atual é o TCC1, a proposta. O TCC2 traz o desenvolvimento completo e a avaliação. Era
preciso definir quais capítulos o TCC1 tem e até onde cada um vai.

## Decisão

O TCC1 tem seis capítulos:

| Cap. | Título | Arquivo |
|---|---|---|
| 1 | Introdução | `editaveis/introducao.tex` |
| 2 | Referencial Teórico | `editaveis/referencial.tex` |
| 3 | Metodologia | `editaveis/metodologia.tex` |
| 4 | Proposta (arquitetura e instanciação no caso) | `editaveis/proposta.tex` |
| 5 | Resultados Preliminares | `editaveis/resultados.tex` |
| 6 | Considerações Finais (inclui o cronograma do TCC2) | `editaveis/consideracoes.tex` |

Os capítulos de instrução do template FGA foram removidos. Dedicatória, agradecimentos, epígrafe,
errata, lista de símbolos, apêndices e anexos ficam comentados no `tcc.tex` e voltam no TCC2, se
fizer sentido.

## Alternativas consideradas

- **Juntar proposta e metodologia num capítulo só:** deixaria a arquitetura, que é a contribuição,
  sem um capítulo próprio.

## Consequências

- Os resultados preliminares do TCC1 são o diagnóstico, os requisitos, a EDA e o desempenho da regra
  vigente. Nenhum modelo precisa estar treinado.
- A divisão do texto em escritas (E1–E13) está no `planejamento.md`.
