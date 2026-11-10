# 0008 — Arquitetura descrita por papéis, sobre um Data Lakehouse em camadas medalhão

- **Data:** 2026-11-10
- **Status:** proposto
- **Proposto por:** Lucas Bottino
- **Aprovado por:** —

## Contexto

A primeira versão do texto descrevia a arquitetura pelas ferramentas do Gov Hub Cidades: "features
no dbt, Python treina, Airflow orquestra, MLflow registra". Isso tem dois problemas:

- prende a contribuição (ver 0002) a uma pilha tecnológica específica;
- não deixa claro em que camada do lakehouse cada artefato de ML fica.

## Decisão

1. A arquitetura opera sobre um **Data Lakehouse** organizado nas camadas **bronze, prata e ouro**
   da arquitetura medalhão:
   - **bronze:** dado bruto como recebido; é também onde os escores do modelo voltam a entrar,
     como qualquer outra fonte;
   - **prata:** dado limpo e harmonizado; painel unificado e rótulo;
   - **ouro:** features *as of t*, escores consolidados e métricas de monitoramento.

   Datasets congelados e artefatos de modelo ficam numa área própria do armazenamento de objetos,
   fora das camadas medalhão. São saídas do treino, não etapas de transformação, e por isso não
   justificam uma camada nova.

2. A arquitetura é descrita por **papéis**, nunca por ferramentas:

   | Papel | Responsabilidade | Não faz |
   |---|---|---|
   | Orquestrador | Agenda e encadeia as etapas; aplica o gate de promoção | Cálculo sobre dados |
   | Camada de transformação | Painel, rótulo, features, leitura dos escores, monitoramento, testes | Treinar modelos |
   | Motor analítico | Materializa e consulta prata e ouro | — |
   | Armazenamento de objetos | Bronze, datasets congelados, artefatos | — |
   | Ambiente de modelagem | Treina, avalia e escora lendo a camada ouro | Recalcular features |
   | Registro de experimentos e modelos | Métricas, versões e estágio dos modelos | Decidir a promoção |
   | Catálogo de dados | Tabelas, responsáveis e linhagem | — |
   | Camada de visualização | Ranking e monitoramento | Calcular métricas |

3. As ferramentas aparecem **uma única vez**, na tabela "Ferramentas que materializam cada papel no
   Gov Hub Cidades" (seção 4.3, *Materialização da arquitetura*). Ferramentas citadas no Referencial
   aparecem só como exemplos de cada papel.

## Alternativas consideradas

- **Descrever direto pelas ferramentas:** mais concreto, mas amarra a contribuição ao Gov Hub e
  dificulta a discussão de generalização (requisito R8, validade externa).
- **Escores gravados direto na camada ouro:** mais simples, mas criaria uma tabela ouro fora do
  fluxo de transformação, sem os testes e o catálogo das demais.

## Consequências

- Os capítulos 1 a 4, o 6, o resumo e o abstract foram reescritos em termos de papéis e camadas. A
  antiga tabela de ferramentas da Metodologia foi removida, e a seção agora aponta para a tabela da
  instanciação.
- A questão QE1 passou a perguntar também em qual camada fica cada artefato de ML.
- Detalha a decisão 0002 sem substituí-la: a ideia central (estender a plataforma existente) continua
  a mesma.
