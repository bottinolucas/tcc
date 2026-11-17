# 0015 — A série legada entra no rótulo, com critérios de aceite por família

- **Data:** 2026-11-16
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

O rótulo de paralisação só é confiável no período SFTP (dez/2019 a nov/2024). Há 1.267
transições antes da troca de fonte (junho de 2024), 980 delas no Rural (levantamento da T1), o que é pouco para treinar e testar com vários cortes temporais. A
recuperação do *dump* legado mostrou que o relatório executivo da Caixa traz a situação da obra de
jul/2015 a ago/2018 (6.942 linhas marcadas como paralisada), com o código APF ligável à fonte atual
em 98% dos casos. O parecer pediu que o texto dissesse o que precisa ser verdade para essa série
entrar, em quanto tempo, e o que fazer sem ela.

## Decisão

A série legada **entra no rótulo**, para ampliar a base de treino. O período rotulado passa a ser o
legado da Caixa (jul/2015 a ago/2018) somado ao SFTP (dez/2019 a nov/2024). Cada família de
relatório só entra se cumprir os cinco critérios:

1. de-para revisado por pessoa das colunas de situação, de percentual de obra e de código APF;
2. ligação do APF com o identificador atual da obra em pelo menos 95% das linhas;
3. regra de desduplicação definida para os APFs com mais de uma linha na mesma competência;
4. escala do percentual harmonizada (0 a 100) e conferida por amostragem;
5. nenhum pico de transições para `paralisada` nos meses de troca de layout. Um pico conta como
   artefato de fonte, como no SFTP para SNH.

O prazo vai até o fim da sprint S2 do TCC2 (11/04/2027). A família que não cumprir os critérios fica
fora do rótulo, e isso é registrado. O Banco do Brasil entra só onde a ponte de códigos existir
(cerca de 200 empreendimentos do FAR).

## Alternativas consideradas

- **Rótulo só no período SFTP:** é seguro, mas tem poucos eventos e um único corte de teste
  razoável.
- **Adiar a decisão para a EDA:** foi a posição da versão de 16/11, e a banca a leu como indecisão.

## Consequências

- O texto troca "a decisão fica para a EDA" por esta decisão e pelos critérios acima.
- A avaliação usa origem móvel (*rolling origin*) com cortes nos dois períodos (ver 0016).
- Entra na tabela de riscos: família reprovada → sai do rótulo e a avaliação fica com menos cortes.
- Fecha a decisão em aberto "usar a série histórica no rótulo?".
