# Planejamento do TCC1

Última atualização: 17/11/2026 (revisão editorial: consistência, formatação e referências)

## 1. Tema

| | |
|---|---|
| **Título** | Arquitetura de MLOps para dados governamentais |
| **Autores** | Lucas Gama De Araujo Bottino e Wallyson Paulo Costa Souza |
| **Etapa** | TCC1 (proposta) |
| **Orientação** | Prof. Dr. Isaque Alves; coorientação: Profa. Dra. Carla Rocha Aguiar e MSc. Guilherme Fernandes |
| **Contribuição** | A arquitetura de MLOps. O caso da paralisação de obras serve para instanciá-la e avaliá-la |
| **Caso** | Prever quais obras em execução do MCMV vão paralisar nos próximos meses (Gov Hub Cidades / MCID), como análise de sobrevivência em tempo discreto (decisão 0014) |
| **Método** | Design Science Research (Hevner, 2004; Peffers et al., 2007) |
| **Fonte de verdade do caso** | `data-application-cidades/docs/adr/0001-arquitetura-mlops-prevencao-paralisacao.md` e `ml/prevencao_paralisacao/README.md` |

**Questão de pesquisa (QP):** como estruturar uma arquitetura de MLOps integrada a uma plataforma
de dados governamentais organizada em camadas medalhão, de modo que os resultados de modelos
preditivos sejam reprodutíveis, rastreáveis e comparáveis à regra vigente sem vazamento temporal?

- **QE1:** o que fica na camada de transformação, no ambiente de modelagem e no orquestrador, e em
  qual camada fica cada artefato de ML?
- **QE2:** como permitir que qualquer resultado seja reproduzido e rastreado até o código, os dados
  e o ambiente?
- **QE3:** a arquitetura permite comparar o modelo com a regra vigente em condições iguais, sem
  vazamento temporal?

**Objetivos específicos:** OE1 requisitos; OE2 projeto por papéis; OE3 instanciação no caso; OE4
avaliar a arquitetura (AV1, AV2, AV8); OE5 avaliar a instanciação (AV3–AV7). O quadro Objetivos ×
Evidências está na metodologia (`tab:objetivos-evidencias`).

**Tese em uma frase:** estender o Data Lakehouse existente em vez de criar uma plataforma de ML
paralela. Painel e rótulo ficam na camada prata; features, escores e monitoramento, na ouro; e os
escores voltam pela bronze. A camada de transformação faz todo o cálculo, o ambiente de modelagem só
treina, avalia e escora, o orquestrador coordena, e cada treino congela um dataset versionado. A
arquitetura é descrita por papéis, e as ferramentas aparecem só na instanciação (decisão 0008).
Na instanciação, a stack é DVC, MLflow com apelidos champion/challenger, validação em três pontos,
ciclo disparado por dados (nível 1 de maturidade) e monitoramento em dois tempos (decisão 0009). O
caso é sobrevivência em tempo discreto (decisão 0014), com o rótulo no legado da Caixa (2015–2018)
e no SFTP (2019–2024) (decisão 0015). A avaliação tem oito critérios com condição de atendimento
(decisão 0016). LLM/RAG entra só como discussão textual (decisão 0013).

## 2. Estrutura e divisão em escritas

Status: ✅ rascunho pronto · 🟡 rascunho com pendências · ⬜ depende de trabalho prático

| # | Escrita | Arquivo | Status | O que falta |
|---|---|---|---|---|
| E1 | Introdução no modelo contexto → objetivos → metodologia → resultados → conclusão | `introducao.tex` | ✅ | Atualizar o parágrafo de resultados com o número da regra (T1) |
| E2–E5, E14 | Referencial: plataformas, ML em produção, MLOps (com figuras), riscos | `referencial.tex` | ✅ | — |
| E15 | Ref. 2.4: LLM reduzida a dois parágrafos (decisão 0013) | `referencial.tex` | ✅ | — |
| E21 | Ref. 2.5.6: sobrevivência em tempo discreto (figura pessoa-período) | `referencial.tex` | ✅ | — |
| E6 | Ref. 2.6: ML no setor público | `referencial.tex` | 🟡 | Ampliar depois da busca de E7 |
| E7 | Ref. 2.7: trabalhos relacionados (+ Amou Najafabadi 2024, Databricks 2023) e protocolo da busca | `referencial.tex` | 🟡 | Executar a busca estruturada e registrar contagens (T1) |
| E8, E18 | Metodologia: DSR (figura), demonstração por reprodução sobre o histórico, AV1–AV8 com condição de atendimento, quadro Objetivos × Evidências, Scrum condensado | `metodologia.tex` | ✅ | Nome do revisor externo |
| E9, E16, E17 | Proposta: requisitos, arquitetura, reprodutibilidade e rastreabilidade, operação (figura), LLM curta | `proposta.tex` | ✅ | — |
| E10 | Proposta: instanciação (sobrevivência, período rotulado, regra vigente no mês t, Tabela 10 com estado) | `proposta.tex` | ✅ | Decisões do MCID (h, k, retomada, usuário) ou valores padrão |
| E11 | Resultados: levantamento dos dados e regra vigente no histórico | `resultados.tex` | ⬜ | Preencher as células `\pendentecelula{T1}` e interpretar (T1) |
| E19 | Resultados: série legada, critérios de aceite (decisão 0015) e figura do pipeline | `resultados.tex` | ✅ | Aplicar os critérios (S1–S2) |
| E12, E20 | Considerações parciais: próximos passos, cronograma S1–S9, riscos | `consideracoes.tex` | ✅ | Refazer o cronograma depois da T2 |
| E13 | Resumo e abstract | `resumo.tex`, `abstract.tex` | ✅ | Acrescentar o número da regra (T1) |

### Ordem sugerida para o que falta

1. **Regra vigente no mês t** no período SFTP, FAR e FDS, com h = 6 e k em 5%, 10% e 20% das obras
   em execução (Tabela `tab:regra-historico`). Definição na Seção 4.3.3; o SQL de origem é
   `ouro_reloginho_indicadores_gargalo_desempenho.sql` (pontuação `score_gargalo` sem o sinalizador
   de paralisação).
2. **Tabela de transições** por modalidade e fonte (`tab:levantamento`) e EDA perguntas 1 a 3.
3. **Integrar ao repositório da plataforma** `ml/` e `docs/adr/0001-*` (hoje só na cópia local,
   não versionados), com PR.
4. **Busca estruturada** (seção 5 abaixo) e contagens no texto.
5. **Decisões em aberto** com o MCID (h, k, retomada, usuário) e revisor externo (orientadores).
6. Revisão com os orientadores e retirada dos `\pendente`.

## 3. Sprints

Scrum adaptado, com sprints de 2 semanas (decisão 0011).
- **PO:** ponto focal do MCID (a confirmar).
- **Time:** a dupla.
- **Stakeholders:** orientador e coorientadores.
- **Backlog:** Issues + GitHub Project neste repositório.

| Sprint | Período | Meta | Status |
|---|---|---|---|
| 0 | 27/10 a 15/11/2026 | Diagnóstico, ADR da arquitetura, especificação do caso, levantamento dos dados, primeira versão do TCC1 e refinamento (stack, LLM, sprints, histórico) | ✅ |
| T1 | 16/11 a 29/11/2026 | Regra vigente no mês t no período SFTP; tabela de transições; EDA perguntas 1 a 3; busca estruturada; integrar `ml/` e ADR 0001 na plataforma | ⬜ |
| T2 | 30/11 a 13/12/2026 | Resultados da T1 no texto (E11); revisão com os orientadores; entrega do TCC1 | ⬜ |
| S1–S9 | TCC2 | Ver a tabela `tab:cronograma` em `consideracoes.tex` (nove sprints entre 15/03 e 16/07/2027) | ⬜ |

**Definição de pronto:**
- código: PR revisado, CI verde, `dbt build`;
- modelo: execução no MLflow com hash DVC;
- texto: compila, sem `\pendente` do item;
- decisão: ADR.

## 4. Artigos escolhidos

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

### Stack de MLOps, LLM, gestão e dados legados (adicionadas em 15/11/2026)

| Ref. | Por que | Onde | Prior. |
|---|---|---|---|
| Barrak, Eghan e Adams (2021), SANER | Estudo empírico de projetos com DVC: o pipeline de dados evolui junto com o código | 2.3 | ○ |
| Chen et al. (2020), DEEM; documentação do MLflow | Registro de modelos, apelidos champion/challenger, tracing de LLM | 2.3 | ○ |
| Pineau et al. (2021), JMLR | O que é preciso registrar para reproduzir um resultado de ML | 2.3, 4.2 | ★ |
| Schelter et al. (2018), PVLDB | Validação de dados como teste unitário | 2.5, 4.2 | ○ |
| Lu et al. (2019), TKDE | Concept drift: detectar, entender, adaptar | 2.5 | ○ |
| Gebru et al. (2021), CACM | Datasheets de datasets | 2.5, 4.2 | ○ |
| Mehrabi et al. (2022), CSUR | Viés e equidade em ML. Base do R9 | 2.5, R9 | ★ |
| Sambasivan et al. (2021), CHI | Cascatas de dados em IA de alto impacto | 2.5, 5.4 | ★ |
| Lewis et al. (2020), NeurIPS; Edge et al. (2024) | RAG e GraphRAG | 2.4 | ○ |
| Es et al. (2024), RAGAS | Avaliar recuperação e geração separadamente | 2.4 | ○ |
| Greshake et al. (2023), AISec; OWASP Top 10 LLM (2025) | Segurança de aplicações com LLM | 2.4 | ○ |
| Schwaber e Sutherland (2020), Scrum Guide | Scrum | 3.4 | ○ |
| Saltz, Shamshurin e Crowston (2017), HICSS | Metodologias de gestão em ciência de dados | 3.4 | ○ |
| Martínez-Plumed et al. (2021), TKDE | CRISP-DM como trajetórias não lineares | 3.4 | ○ |
| Buneman, Khanna e Tan (2001), ICDT | Proveniência de dados | 5.4 | ○ |
| Wang e Strong (1996), JMIS | Dimensões de qualidade de dados | 5.4 | ○ |
| Rahm e Bernstein (2001), VLDB J.; Curino et al. (2008), PVLDB | Schema matching e evolução de esquema (de-para de colunas do histórico) | 5.4 | ○ |

### Adicionadas em 16/11/2026 (revisão pós-devolutiva)

| Ref. | Por que | Onde | Prior. |
|---|---|---|---|
| Kaplan e Meier (1958); Singer e Willett (2003); Tutz e Schmid (2016) | Sobrevivência; tempo discreto e formato pessoa-período | 2.5.6, 4.3 | ★ |
| Harrell, Lee e Mark (1996); Graf et al. (1999) | C-index e Brier integrado | 2.5.6, 4.3 | ○ |
| Fine e Gray (1999) | Riscos competitivos (conclusão × paralisação) | 2.5.6, 5.8 | ○ |
| Davidson-Pilon (2019), lifelines | Biblioteca de sobrevivência na instanciação | Tabela 10 | ○ |
| Amou Najafabadi et al. (2024), ECSA | Mapeamento de 43 estudos, 35 componentes de arquiteturas de MLOps | 2.7 | ★ |
| Databricks (2023), Big Book of MLOps | Literatura cinzenta: dados e ativos de ML no mesmo lakehouse | 2.7 | ★ |

### Adicionadas em 17/11/2026 (revisão editorial; conferidas na fonte, ainda não lidas pelos autores)

| Ref. | Por que | Onde | Prior. |
|---|---|---|---|
| Siddiqi (2006); Yurdakul (2018) | Origem dos limiares 0,1 e 0,25 do PSI e suas propriedades estatísticas | 2.5, 4.2.6 | ○ |
| Grinsztajn, Oyallon e Varoquaux (2022), NeurIPS | Gradient boosting continua entre os melhores em dados tabulares | 2.5 | ○ |
| Veale e Brass (2019); Engstrom et al. (2020) | ML na administração pública: níveis de gestão e levantamento em agências federais | 2.6 | ○ |
| Brasil (2021), EBIA (Portaria MCTI 4.617) | Aplicação de IA no poder público como eixo da estratégia nacional | 2.6 | ○ |
| Gil (2002) | Classificação da pesquisa | 3.1 | ○ |
| van Houwelingen (2007) | Predição por marco (landmark) em sobrevivência: features fixadas em t e deslocamento j | 4.3.1 | ★ |

## 5. Busca estruturada pendente (E7)

| Base | String |
|---|---|
| Scopus / IEEE Xplore / ACM DL | `"MLOps" AND ("public sector" OR "government" OR "public administration")` |
| Scopus / ASCE Library | `("machine learning" OR "predictive") AND ("construction" OR "public works") AND ("delay" OR "stoppage" OR "abandon*")` |
| SBC OpenLib / BDTD | `"aprendizado de máquina" AND ("obras públicas" OR "obras paralisadas")` |

Critérios: 2015 em diante; estudo empírico ou proposta de arquitetura; texto completo disponível.
Registrar quantos trabalhos cada string retornou e quantos foram selecionados.

## 6. Decisões

As decisões tomadas e as que estão em aberto ficam em [`decisoes/`](decisoes/README.md), uma por
arquivo. Uma decisão só passa a aceita quando os dois autores concordam.
