# 0014 — Formulação do caso: análise de sobrevivência em tempo discreto

- **Data:** 2026-11-16
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

A versão de 16/11 do TCC1 tratava a paralisação como classificação binária (LightGBM) e deixava a
análise de sobrevivência como alternativa, "se a EDA mostrar". A dupla decidiu que o caso é de
sobrevivência: o que interessa à fiscalização é quanto tempo falta até a obra paralisar, e boa parte
das obras termina a série sem paralisar (censura). O painel já existe com grão obra × mês e as
features são calculadas *as of* t, o que corresponde ao formato pessoa-período da análise de
sobrevivência em tempo discreto (Singer e Willett, 2003; Tutz e Schmid, 2016).

## Decisão

1. **Unidade e evento.** Cada obra em execução (`em_obras`) no mês t contribui com uma linha. O
   evento é a primeira passagem para `paralisada`.
2. **Censura.** Conclusão, cancelamento e fim do período rotulado censuram a obra. Conclusão e
   cancelamento são, a rigor, riscos competitivos. Isso fica registrado como ameaça e como análise
   de sensibilidade.
3. **Truncamento à esquerda.** Obras que entram no painel já em execução entram no conjunto de risco
   só a partir do primeiro mês observado. A lacuna entre a série legada e o SFTP (set/2018 a
   nov/2019) é tratada como entrada tardia: a obra volta ao conjunto de risco em dez/2019 se ainda
   estiver em execução.
4. **Modelos.** As linhas de base são Kaplan-Meier, por modalidade, e Cox. O modelo principal é
   gradient boosting (LightGBM) sobre o risco discreto mensal, com explicações SHAP.
5. **Saída e métricas.** O escore de cada obra é o risco acumulado até o horizonte h,
   P(paralisar até t+h). As métricas principais são recall@k e precision@k nesse horizonte, por
   serem comparáveis à regra vigente. As secundárias são C-index e Brier integrado.

## Alternativas consideradas

- **Classificação binária com janela fixa:** descarta o tempo até o evento e trata mal as obras
  censuradas antes de t+h.
- **Sobrevivência em tempo contínuo (Cox e Random Survival Forest):** o dado é mensal, e as features
  variam no tempo. O formato pessoa-período encaixa direto nas tabelas *as of* t da camada ouro.

## Consequências

- Complementa a 0004. O caso continua o mesmo, e muda a formulação.
- O rótulo na camada prata passa a ser o par (tempo, evento) por obra e mês, com a censura
  explícita.
- Entram no Referencial uma subseção sobre sobrevivência em tempo discreto e as referências
  correspondentes. lifelines (ou scikit-survival) entra no ambiente de modelagem.
