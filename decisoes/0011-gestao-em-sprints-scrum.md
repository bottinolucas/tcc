# 0011 — Gestão do trabalho em sprints (Scrum adaptado a dados)

- **Data:** 2026-11-15
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

O TCC não tinha um planejamento do trabalho além de um cronograma "Mês 1 a Mês 6". A ideia é
organizar o trabalho como numa equipe de produto, com ciclos curtos, papéis e critério de pronto.
Scrum puro, porém, foi pensado para entregar funcionalidades, e boa parte deste trabalho é
exploratória.

## Decisão

1. **Scrum** (Schwaber e Sutherland, 2020) com **sprints de 2 semanas**, adaptado a dados (Saltz et
   al., 2017; Martínez-Plumed et al., 2021):
   - meta de sprint como hipótese nas sprints de exploração;
   - investigações com prazo fixo;
   - fases do CRISP-DM como épicos, sem cascata;
   - duas trilhas no mesmo backlog: plataforma e escrita.
2. **Papéis:**
   - PO: ponto focal técnico do MCID (a confirmar);
   - time: os dois autores;
   - Scrum Master: revezamento por sprint;
   - stakeholders: orientadora e coorientador, na review.
3. **Definição de pronto em camadas:**
   - código: PR revisado, CI verde, `dbt build`;
   - modelo: execução no MLflow com hash DVC;
   - texto: compila, sem `\pendente` do item;
   - decisão: ADR.
4. **Backlog:** Issues + GitHub Project no próprio `bottinolucas/tcc`, com campos Sprint e Épico
   (A1–A7, E1–E13). Os itens da plataforma apontam para as issues e os PRs do
   `data-application-cidades`. Acompanhamento por burnup.
5. **Calendário:**
   - Sprint 0: 27/10 a 15/11/2026, o TCC1 feito até aqui;
   - T1 e T2: duas sprints até a entrega do TCC1, em dezembro/2026;
   - S1 a S12: TCC2.

## Alternativas consideradas

- **Kanban com marcos mensais:** mais leve, porém menos próximo da rotina de uma equipe de produto.
- **Sprints de 1 semana:** cerimônias demais para uma dupla com outras disciplinas.
- **Repositório separado para o backlog:** o `bottinolucas/tcc` já é só do TCC.

## Consequências

- Metodologia: nova seção *Planejamento e gestão do trabalho* (`sec:gestao`).
- Considerações: o cronograma passa a ser a tabela de sprints S1–S12.
- Criar o Project e as issues no GitHub depende de confirmação do Lucas.
