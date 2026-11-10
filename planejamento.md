# Planejamento do TCC1

Última atualização: 10/11/2026

## 1. Tema

| | |
|---|---|
| **Título** | Arquitetura de MLOps para dados governamentais |
| **Autores** | Lucas Gama De Araujo Bottino e Wallyson Paulo Costa Souza |
| **Etapa** | TCC1 (proposta) |
| **Orientação** | Profa. Dra. Carla Rocha Aguiar; coorientação: Prof. Dr. Isaque Alves |
| **Contribuição** | A arquitetura de MLOps. O caso da paralisação de obras serve para instanciá-la e avaliá-la |
| **Caso** | Prever quais obras ativas do MCMV vão paralisar nos próximos meses (Gov Hub Cidades / MCID) |
| **Método** | Design Science Research (Hevner, 2004; Peffers et al., 2007) |
| **Fonte de verdade do caso** | `data-application-cidades/docs/adr/0001-arquitetura-mlops-prevencao-paralisacao.md` e `ml/prevencao_paralisacao/README.md` |

**Questão de pesquisa (QP):** como estruturar uma arquitetura de MLOps que se integre a uma
plataforma de dados governamentais existente, garantindo reprodutibilidade, rastreabilidade e
avaliação honesta de modelos?

- **QE1:** o que fica no dbt, o que fica no Python e o que fica no Airflow?
- **QE2:** como garantir que qualquer resultado possa ser refeito a partir do código e dos dados?
- **QE3:** a arquitetura permite comparar o modelo com a regra vigente sem vazamento temporal?

**Tese em uma frase:** estender o Data Lakehouse existente em vez de criar uma plataforma de ML
paralela. Painel e rótulo ficam na camada prata; features, escores e monitoramento, na ouro; e os
escores voltam pela bronze. A camada de transformação faz todo o cálculo, o ambiente de modelagem só
treina, avalia e escora, o orquestrador coordena, e cada treino congela um dataset versionado. A
arquitetura é descrita por papéis, e as ferramentas aparecem só na instanciação (decisão 0008).

## 2. Estrutura e divisão em escritas

Status: ✅ rascunho pronto · 🟡 rascunho com pendências · ⬜ depende de trabalho prático

| # | Escrita | Arquivo | Status | O que falta |
|---|---|---|---|---|
| E1 | Introdução: contexto, problema, questões, objetivos | `introducao.tex` | ✅ | Revisar depois de E11 |
| E2 | Ref. 2.1: plataformas de dados (camadas, lakehouse, Airflow/dbt) | `referencial.tex` | ✅ | — |
| E3 | Ref. 2.2: ML em produção (dívida técnica, desafios, CRISP-DM) | `referencial.tex` | ✅ | — |
| E4 | Ref. 2.3: MLOps (P1–P9, maturidade, MLflow, ML Test Score) | `referencial.tex` | ✅ | — |
| E5 | Ref. 2.4: riscos com dados longitudinais (vazamento, validação temporal, skew, recall@k, drift) | `referencial.tex` | ✅ | — |
| E6 | Ref. 2.5: ML no setor público | `referencial.tex` | 🟡 | Seção curta; ampliar depois da busca de E7 |
| E7 | Ref. 2.6: trabalhos relacionados e tabela comparativa | `referencial.tex` | 🟡 | Busca estruturada (ver seção 4) |
| E8 | Metodologia: DSR, contexto, critérios AV1–AV5, ferramentas | `metodologia.tex` | 🟡 | Equipe e vínculo com o MCID; decidir se haverá avaliação qualitativa |
| E9 | Proposta: requisitos R1–R8, arquitetura, responsabilidades, ciclo de vida | `proposta.tex` | 🟡 | Limiares de drift e política de retreino |
| E10 | Proposta: instanciação no caso MCMV | `proposta.tex` | 🟡 | Decisões sobre h, k, retomada e usuário do alerta |
| E11 | Resultados preliminares: diagnóstico, EDA, ameaças à validade | `resultados.tex` | ⬜ | Rodar a EDA e calcular o recall@k da regra vigente |
| E12 | Considerações finais e cronograma do TCC2 | `consideracoes.tex` | 🟡 | Meses reais do semestre |
| E13 | Resumo e abstract | `resumo.tex`, `abstract.tex` | ✅ | Ajustar depois de E11 |

### Ordem sugerida para o que falta

1. **E10**: fechar h, k, retomada e usuário do alerta. Isso trava a EDA e a métrica.
2. **E11**: recall@k da regra vigente no período SFTP. Dá para calcular sem nenhum modelo e é o
   resultado preliminar mais forte para a banca.
3. **E11**: EDA, perguntas 1 a 3 (cobertura, troca de fonte, de-para de situação), com as figuras.
4. **E7 e E6**: busca estruturada e ampliação dos trabalhos relacionados.
5. **E8, E9, E12**: pendências curtas (equipe, drift, cronograma).
6. **E1 e E13**: revisão final de introdução, resumo e abstract com os resultados em mãos.
7. Revisão com os orientadores.

## 3. Artigos escolhidos

Todas as referências abaixo estão em `bibliografia.bib` e tiveram autoria e veículo conferidos.
**Prioridade de leitura:** ★ ler inteiro (sustenta o argumento) · ○ consulta pontual (sustenta uma
afirmação).

### Núcleo do argumento

| Ref. | Por que está no trabalho | Onde | Prior. |
|---|---|---|---|
| Sculley et al. (2015), *Hidden Technical Debt in ML Systems* | Mostra que o código de ML é a menor parte do sistema e que a dívida está em dados, pipelines e configuração. Base da motivação e do R1 | Intro, 2.2, R1 | ★ |
| Kreuzberger, Kühl e Hirschl (2023), *MLOps: Overview, Definition, and Architecture* | Definição de MLOps e os princípios P1–P9, que são o critério AV1 | 2.3, AV1, R3/R4/R6 | ★ |
| Paleyes, Urma e Lawrence (2022), *Challenges in Deploying ML* | Desafios de implantação em cada etapa, a partir de casos reais | Intro, 2.2 | ★ |
| Ferreira, Silva, Rocha e Pinto (2025), *From Pre-labeling to Production* | ML no setor público brasileiro (Brasil Participativo) visto como problema de engenharia institucional. Coautoria da orientadora | Intro, 2.5, 2.6, R7 | ★ |
| Aguiar (2020), *Desafios na adoção de MLOps por time DevOps* | Relato de MLOps em parceria governo–academia. Autoria da orientadora | 2.3, 2.6 | ★ |
| Kaufman et al. (2012), *Leakage in Data Mining* | Definição de vazamento. Base do R2 e do AV4 | 2.4, R2 | ★ |

### Metodologia

| Ref. | Por que | Onde | Prior. |
|---|---|---|---|
| Hevner et al. (2004), *Design Science in IS Research* | Fundamento da DSR | Intro, Cap. 3 | ★ |
| Peffers et al. (2007), *A DSR Methodology for IS Research* | As seis atividades que organizam o trabalho (Tabela 2) | Cap. 3 | ★ |
| Hevner (2007), *A Three Cycle View of DSR* | Ciclos de relevância, rigor e design | Cap. 3 | ○ |
| Wieringa (2014), *Design Science Methodology* | Leitura de apoio sobre DSR em Engenharia de Software | (bib) | ○ |

### Ciclo de vida e operação

| Ref. | Por que | Onde | Prior. |
|---|---|---|---|
| Wirth e Hipp (2000), CRISP-DM | Fases que organizam as pastas `ml/<modelo>/` | 2.2, Tabela 7 | ○ |
| Studer et al. (2021), CRISP-ML(Q) | Acrescenta monitoramento e garantia de qualidade. Base do gate (R5) | 2.2, R5 | ★ |
| Amershi et al. (2019), *SE for ML: A Case Study* | Fluxo de ML em nove etapas na Microsoft; dados mais difíceis de gerir que código. Base do R8 | 2.2, R8 | ○ |
| Lwakatare et al. (2020) | Desafios de ML em larga escala na indústria | 2.2 | ○ |
| Shankar et al. (2024), *We Have No Idea How Models will Behave...* | Velocidade, validação e versionamento como fatores de sucesso | 2.2, R3 | ○ |
| Breck et al. (2017), *The ML Test Score* | Rubrica de prontidão para produção. É o critério AV2 | 2.3, AV2, R5 | ★ |
| John, Olsson e Bosch (2021), *Towards MLOps: Framework and Maturity Model* | Modelo de maturidade | 2.3 | ○ |
| Google Cloud (2020), níveis de maturidade de MLOps | Níveis 0, 1 e 2 | 2.3 | ○ |
| Testi et al. (2022), *MLOps: A Taxonomy and a Methodology* | Taxonomia de MLOps | 2.3 | ○ |
| Zaharia et al. (2018), MLflow | Rastreamento de experimentos e registro de modelos | 2.3, R4 | ○ |
| Polyzotis et al. (2018), *Data Lifecycle Challenges* | Training-serving skew. Base do R1 | 2.4, R1 | ○ |
| Breck et al. (2019), *Data Validation for ML* | Validação de dados com esquemas | 2.4 | ○ |
| Gama et al. (2014); Rabanser et al. (2019) | Concept drift e detecção de mudança de distribuição. Base do R6 | 2.4, R6 | ○ |

### Modelagem e avaliação do caso

| Ref. | Por que | Onde | Prior. |
|---|---|---|---|
| Bergmeir e Benítez (2012) | Validação em dados temporais | 2.4 | ○ |
| Saito e Rehmsmeier (2015) | Curva precisão-revocação em classes desbalanceadas | 2.4, 4.3 | ○ |
| Ke et al. (2017), LightGBM | Primeira família de modelos | 2.4, 4.3 | ○ |
| Lundberg e Lee (2017), SHAP | Explicação do escore para a fiscalização | 2.4, 4.3 | ○ |
| Mitchell et al. (2019), *Model Cards* | Documentação do modelo | 2.4, 4.3 | ○ |
| Cox (1972); Wang, Li e Reddy (2019) | Alternativa por análise de sobrevivência | 2.4, 4.3 | ○ |

### Domínio e trabalhos relacionados

| Ref. | Por que | Onde | Prior. |
|---|---|---|---|
| TCU, Acórdão 1079/2019 | Dimensão do problema: 14.403 de 38.412 obras paralisadas | Intro | ○ |
| Madaio et al. (2016), *Firebird* | O análogo mais próximo: escore de risco para priorizar inspeções com capacidade limitada | 2.6 | ★ |
| Gondia et al. (2020) | ML para prever risco de atraso em obras | 2.6 | ○ |
| Fernandes (2024), TCC UFCG | XGBoost para prever fracasso de obras públicas na Paraíba (dados do SAGRES/TCE-PB) | 2.6 | ○ |
| Wirtz, Weyerer e Geyer (2019) | Desafios de IA no setor público | 2.5 | ○ |
| Janssen et al. (2012) | Benefícios e barreiras dos dados abertos | Intro | ○ |
| Armbrust et al. (2021), Lakehouse; Reis e Housley (2022) | Fundamentos de engenharia de dados | 2.1 | ○ |
| Leis e decretos (LGPD, Dados Abertos, Governo Digital, MCMV) | Base normativa | Intro, 2.5 | ○ |

## 4. Busca estruturada pendente (E7)

| Base | String |
|---|---|
| Scopus / IEEE Xplore / ACM DL | `"MLOps" AND ("public sector" OR "government" OR "public administration")` |
| Scopus / ASCE Library | `("machine learning" OR "predictive") AND ("construction" OR "public works") AND ("delay" OR "stoppage" OR "abandon*")` |
| SBC OpenLib / BDTD | `"aprendizado de máquina" AND ("obras públicas" OR "obras paralisadas")` |

Critérios: 2015 em diante; estudo empírico ou proposta de arquitetura; texto completo disponível.
Registrar quantos trabalhos cada string retornou e quantos foram selecionados.

## 5. Decisões

As decisões tomadas e as que estão em aberto ficam em [`decisoes/`](decisoes/README.md), uma por
arquivo. Uma decisão só passa a aceita quando os dois autores concordam.
