# 0016 — Avaliação com condições de sucesso, ligação aos requisitos e reprodução sobre o histórico

- **Data:** 2026-11-16
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

O parecer do TCC1 apontou quatro problemas na avaliação:

1. nenhum critério dizia o que conta como atendido;
2. R1, R5, R6, R7 e R8 não eram verificados por nenhum critério;
3. "rastreabilidade" estava na pergunta sem critério;
4. o "antes" do ML Test Score é zero por construção, porque a plataforma não tinha ML.

Também perguntou como demonstrar retreino mensal e desempenho realizado num semestre, e como uma
regra que "só sinaliza" vira um ranking calculado no passado.

## Decisão

**Critérios**, cada um com uma condição de falha:

| ID | Critério | Requisitos | Atendido quando | Quem aplica |
|---|---|---|---|---|
| AV1 | Aderência a P1–P9 (Kreuzberger et al., 2023) | R4, R5, R6, R7 | cada princípio relevante ao nível 1 de maturidade tem um componente, ou uma justificativa aceita pelo revisor | autores; revisão externa |
| AV2 | Prontidão: ML Test Score com alvo | R1, R5, R6 | nota ≥ 2 em cada uma das quatro seções, sobre os testes aplicáveis ao nível 1 | autores; revisão externa |
| AV3 | Reprodutibilidade | R3 | a reexecução em ambiente limpo reproduz métricas e predições, dentro de tolerância numérica | autores (automatizado) |
| AV4 | Ausência de vazamento temporal | R2 | os testes passam **e** um vazamento injetado de propósito é detectado | autores (automatizado) |
| AV5 | Comparação com a regra vigente | R5 | o protocolo roda de ponta a ponta a partir de artefatos versionados; o resultado do modelo é reportado seja qual for | autores |
| AV6 | Equidade | R9 | a diferença de recall@k entre subgrupos é calculada e monitorada para o modelo e para a regra | autores |
| AV7 | Rastreabilidade | R4, R7 | para uma amostra de escores na camada ouro, a cadeia escore → versão do modelo → execução → hash do dataset → commit → tabelas de origem se reconstrói sem elo faltando | autores; revisão externa |
| AV8 | Extensibilidade | R8 | a regra vigente entra como segundo escorador na mesma estrutura, sem alterar nenhum artefato do primeiro modelo (diff vazio) | autores |

**Revisor externo.** Um integrante da equipe do Gov Hub que não seja autor revisa AV1, AV2 e AV7.

**Regra vigente no mês t.** A comparação parte do SQL real
(`ouro_reloginho_indicadores_gargalo_desempenho`), que já calcula uma pontuação ponderada
(`score_gargalo`, de 0 a 9). A definição tem quatro partes:

- a pontuação é recalculada com `current_date` trocado pelo último dia do mês t, e só com registros
  disponíveis até t;
- o sinalizador de paralisação é excluído, porque a população são as obras em execução;
- as obras são ordenadas pela pontuação, com desempate por dias sem atualização e por dias de
  atraso;
- k é tratado como faixa enquanto o MCID não o fixar.

A regra cobre só FAR e FDS, e a comparação direta fica restrita a essas modalidades.

**Demonstração.** A operação contínua é reproduzida sobre o histórico, com *backfill* do
orquestrador, mês a mês, sobre as competências do período rotulado. Em cada competência roda o ciclo
disparado por dados: export, escore, retreino com gate e PSI. O desempenho realizado é calculado
onde t+h já tem rótulo. O ciclo conta como executado quando todas as competências do *backfill*
tiverem escore e PSI registrados, e as decisões do gate estiverem no registro de modelos.

**Protocolo do AV5.** Origem móvel com cortes no legado e no SFTP, e intervalo de confiança do
recall@k por *bootstrap*.

**PSI.** Os limiares iniciais são 0,1 (atenção) e 0,25 (alerta), a recalibrar na EDA.

## Alternativas consideradas

- **Manter o ML Test Score "antes e depois":** o "antes" é zero por construção e não informa
  nada.
- **Deixar o R8 só na discussão:** foi o que o parecer criticou. Implementar a regra como segundo
  escorador custa pouco, porque o cálculo dela no mês t é necessário de qualquer forma.

## Consequências

- Substitui a 0006. A 0012 (R9 e AV6) continua valendo.
- A Tabela 4 se divide em duas (procedimento; verificação). Entra o quadro Objetivos × Evidências.
- AV3, AV4, AV7 e AV8 são verificados na sprint em que cada peça é construída. A S7 consolida AV1,
  AV2, AV5 e AV6.
