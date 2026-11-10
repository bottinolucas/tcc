# 0007 — Convenções de escrita, referências e compilação

- **Data:** 2026-11-10
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

Duas pessoas escrevem o mesmo documento, pelo Overleaf e pelo repositório, que se sincronizam nos
dois sentidos por uma GitHub Action. Sem convenções comuns, o texto perde consistência e as
referências ficam difíceis de conferir.

## Decisão

1. **Texto pendente** é marcado com `\pendente{descrição}`, que aparece em vermelho no PDF. Antes da
   entrega, a busca por `\pendente` precisa voltar vazia.
2. **Citações** seguem o abnTeX2 no estilo autor-data: `\cite{chave}` para citação entre parênteses
   e `\citeonline{chave}` para citação no fluxo da frase.
3. **Só entram referências verificadas.** Autoria, veículo, ano e páginas são conferidos na fonte
   antes de ir para o `bibliografia.bib`. Nenhuma referência é citada sem ter sido lida pelo menos
   no resumo.
4. **Autores institucionais** são escritos em maiúsculas, como pede a ABNT (`{{BRASIL}}`).
   Sobrenomes acentuados usam comandos LaTeX, para não quebrarem quando aparecem em caixa alta
   (`K{\"{u}}hl`).
5. **Cada capítulo fica no seu próprio arquivo** em `editaveis/`. Para evitar conflitos, os dois
   autores não editam o mesmo capítulo ao mesmo tempo.
6. **A compilação** usa pdflatex e bibtex, igual ao Overleaf. Antes de enviar, o documento precisa
   compilar sem erros e sem citações indefinidas.
7. **Push na `main`** sincroniza com o Overleaf. Só vai para a `main` o que compila.

## Alternativas consideradas

- **Comentários `%` para marcar pendências:** não aparecem no PDF e acabam esquecidos.

## Consequências

- Revisar o texto dá trabalho, mas cada afirmação apoiada numa referência pode ser rastreada até a
  fonte.
