# 0017 — Estrutura e convenções depois da devolutiva do TCC1

- **Data:** 2026-11-16
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

O parecer e a devolutiva de 16/11/2026, e a conversa com o orientador, trouxeram ajustes de
estrutura e de escrita que valem para o documento inteiro.

## Decisão

1. **Orientação.** O orientador é o prof. Dr. Isaque Alves. Os coorientadores são a profa. Dra.
   Carla Rocha Aguiar e o MSc. Guilherme Fernandes.
2. **Introdução.** Segue o modelo contexto → objetivos → metodologia → resultados iniciais e
   esperados → conclusão. A conclusão da introdução traz a contribuição em um parágrafo e a
   organização dos capítulos.
3. **Capítulo final do TCC1:** "Considerações parciais".
4. **Subseções.** Toda seção que se divide em subseções começa com uma introdução breve. A redução
   do número de subseções fica para uma discussão posterior com o orientador.
5. **Figuras.** O documento usa mais figuras. As figuras tiradas de artigos são redesenhadas em
   TikZ, em português, com "Fonte: adaptada de …".
6. **Termos.**
   - "regra vigente" é o único nome da regra de fiscalização atual;
   - "previsão de paralisação" se refere ao modelo, e "prevenção" só à ação da fiscalização;
   - o capítulo de Proposta descreve o projeto, e o estado de cada peça (já existia, criada no
     TCC1, prevista) fica explícito.
7. **Formatação.**
   - nenhum `Overfull \hbox` no log;
   - tabelas com `@{}` nas bordas e colunas `\raggedright`;
   - identificadores longos com `\cod{}`, que quebra em `_` e `/`;
   - páginas de floats alinhadas no topo.

## Alternativas consideradas

- **Remover já todas as subseções:** o orientador deixou para discutir depois.

## Consequências

- Complementa a 0005 e a 0007.
- Pré-textuais (capa, folha de rosto, ficha), introdução e capítulo 6 são reescritos.
