# Mineiração de Dados — Idosos que moram sozinhos e internações hospitalares

Pesquisa que cruza bases públicas de saúde para investigar se idosos que
moram sozinhos são internados com mais frequência do que idosos que não
moram sozinhos.

**Hipótese:** quando um idoso mora sozinho, um evento como uma queda ou uma
confusão mental demora mais para ser percebido e socorrido, o que leva a
internações mais frequentes por causas que uma presença humana por perto
poderia ter prevenido ou atenuado.

**Status: pipeline completo e testado de ponta a ponta com dado real** — os
5 notebooks rodam sem erro e já produzem resultados (ver
[`data/external/FONTES_RIO_CLARO.md`](data/external/FONTES_RIO_CLARO.md)
para a origem exata de cada fonte).

## Estrutura do estudo (dois níveis)

- **Nível 1 — Estado de São Paulo** (645 municípios): estudo ecológico,
  cruzando IBGE (Censo 2022) e DATASUS (SIH/SUS), com o IDH municipal como
  controle.
- **Nível 2 — Rio Claro**: estudo de caso aprofundado, com dados do
  Cadastro Único obtidos junto à Prefeitura (renda, composição domiciliar).

## Fontes de dados

| Fonte | O que fornece | Cobertura |
|---|---|---|
| IBGE — Censo 2022 (SIDRA, tabela 9879) | Domicílios com responsável idoso e quantos são unipessoais (idoso mora sozinho), por município | 645/645 municípios |
| DATASUS — SIH/SUS (TabNet, **por local de residência**) | Internações de idosos por capítulo CID-10, por município, Jan/2022-Jul/2026 | 645/645 municípios |
| Atlas Brasil | IDH municipal (controle) | 259/645 municípios |
| CadÚnico de Rio Claro (Ofício SMDS nº 2235/2026) | Renda, composição domiciliar (Nível 2) | Só Rio Claro, só famílias de baixa renda |

**Cruzamento por nome:** nenhuma dessas fontes trouxe um código IBGE de 7
dígitos utilizável em conjunto com as outras, e não há acesso à internet no
ambiente de desenvolvimento para baixar a lista oficial do IBGE. Por isso
todo o cruzamento é feito por **nome de município normalizado**
(`config.normalizar_municipio`) — validado com taxa de correspondência muito
alta (645/645 no SIH, 259/260 no IDH; ver `FONTES_RIO_CLARO.md`).

## Como rodar

1. Instale as dependências (Anaconda Prompt, na raiz do projeto):
   ```
   pip install -r requirements.txt
   ```
   Se `geopandas` falhar pelo pip, instale via conda (só é necessário para
   o mapa opcional do notebook 04):
   ```
   conda install -c conda-forge geopandas
   ```
2. Coloque os arquivos de entrada em `data/external/` com os nomes exatos
   listados em [`data/external/README.md`](data/external/README.md).
3. Abra o Jupyter:
   ```
   jupyter notebook
   ```
4. Rode os notebooks **em ordem**, dentro de `notebooks/`:

   | Notebook | O que faz | Saída |
   |---|---|---|
   | `01_coleta_ibge_censo.ipynb` | Idosos sozinhos por município (Censo 2022, tabela 9879) | `censo_domicilios_sp.csv` |
   | `02_coleta_datasus_sih.ipynb` | Internações de idosos por capítulo CID-10 (SIH/SUS por residência) | `internacoes_sp.csv` |
   | `03_integracao_limpeza.ipynb` | Junta tudo por nome de município; gera a base bruta e a base **limpa** | `dataset_municipios_sp_bruto.csv`, `dataset_municipios_sp.csv` |
   | `04_analise_estatistica.ipynb` | Correlação, regressão, **tabela de robustez** (6 especificações), mapa opcional | figuras + `regressao_ols.txt` + `robustez_especificacoes.csv` |
   | `05_estudo_caso_rio_claro.ipynb` | Posição de Rio Claro no estado, perfil de causas, CadÚnico | figuras |

## Três pontos metodológicos importantes

### 1. Correção "local de residência" (notebook 02)

A primeira coleta do SIH usou, por engano, a página do TabNet "por local de
**internação**" — que conta a internação no município do *hospital*, não no
do *paciente*. Isso invalidava o cruzamento geográfico do estudo inteiro.
Corrigido para "por local de **residência**". O total do estado quase não
mudou (~488 mil internações), mas a distribuição entre municípios mudou
completamente: de ~313 para **645** municípios com ao menos uma internação
(Pariquera-Açu estava 7x inflada; Poá e Peruíbe apareciam com zero).
**Reportar essa correção na Metodologia do artigo.**

### 2. Uma linha por município (notebook 03)

`pct_idosos_sozinhos` vem do Censo 2022 e é constante no tempo. Testar a
hipótese num painel por ano inflaria o "n" artificialmente
([pseudorreplicação](https://en.wikipedia.org/wiki/Pseudoreplication)) sem
acrescentar informação. Além disso, os exports atuais do TabNet trazem o
total do período, sem quebra anual — por isso não há análise de série
temporal (para tê-la, re-exportar com Coluna = "Ano processamento").

### 3. Limpeza (notebook 03, seção 3.3)

Três tratamentos antes de gerar `dataset_municipios_sp.csv`:
1. Arredondamento das taxas (2 casas decimais — sem perda de informação real)
2. Remoção de outliers pela regra de Tukey (acima de Q3 + 1,5×IQR) — 25
   municípios, predominantemente muito pequenos, onde o denominador baixo
   deixa a taxa por 100 mil instável
3. Remoção de municípios sem IDH (386) — decisão de eliminar em vez de
   imputar, já que ~60% da coluna está ausente

Isso reduz a base de 645 para **250 municípios**. A versão sem filtros fica
em `dataset_municipios_sp_bruto.csv` e entra na checagem de robustez.

## Resultados (estado atual)

**Modelo principal** (OLS, n=250, controlando por IDH):

| Variável | Coeficiente | p |
|---|---|---|
| `pct_idosos_sozinhos` | +171,8 | **0,042** |
| `idhm` | −41.300 | <0,001 |

R² = 0,080.

**Mas o resultado não é robusto.** O notebook 04 (seção 4.4) roda o mesmo
teste em 6 especificações:

| Especificação | Direção | p<0,05 |
|---|---|---|
| 1. OLS (principal) | positiva | sim |
| 2. OLS, erros robustos HC3 | positiva | não (0,071) |
| 3. OLS + porte do município | positiva | não (0,054) |
| 4. OLS na base bruta (n=259) | positiva | sim (0,011) |
| 5. Binomial negativa (offset) | positiva | sim (0,046) |
| 6. Poisson robusto (offset) | **NEGATIVA** | sim (0,022) |

A inversão do Poisson não é bug: esse modelo pondera cada município pelo
volume de internações, e os 5 maiores concentram ~38% do total — ele acaba
medindo o padrão *entre as grandes cidades*. Testamos formalmente se a
associação muda conforme o porte (termo de interação, seção 4.4b): **não é
significativo** (p=0,49), então não dá para afirmar moderação por porte.

**Leitura honesta:** há evidência **fraca e na direção prevista**, sensível à
forma de modelar. É bem diferente do resultado com o dado errado (por local
de internação), onde não havia associação nenhuma (r=0,037; p=0,565) — mas
também não autoriza afirmar associação estabelecida. **Reportar a tabela de
robustez inteira no artigo**, não só a especificação favorável: um artigo que
mostra a fragilidade e a discute passa por revisão muito melhor.

## Como trabalhar nisso comigo

O pipeline roda de ponta a ponta com o dado que temos. Se rodar um notebook e
algo sair diferente do esperado, me manda a mensagem completa (ou o que
apareceu na tela) que eu ajusto com base nisso.

Melhorias possíveis, em ordem de impacto:
1. **Re-exportar o SIH com Coluna = "Ano processamento"** — devolve a análise
   temporal (evolução da taxa, tendência de Rio Claro)
2. **Completar o IDH** para os ~386 municípios que faltam — hoje a análise
   principal perde 60% da amostra por isso
3. **Microdados via `pysus`** (notebook 02, seção 2.3) — permitiria usar a
   subcategoria exata da CID-10 (W00-W19 para quedas) em vez do capítulo
   inteiro. Só roda localmente, fora deste ambiente

## Estrutura de pastas

```
data/
├── raw/         # baixado automaticamente pelos notebooks (não versionado)
├── external/    # baixado manualmente por você (não versionado, exceto os .md)
└── processed/   # gerado pelos notebooks — datasets consolidados (não versionado)
notebooks/       # os 5 notebooks, na ordem de execução
src/config.py    # constantes, normalização de nomes e caminhos compartilhados
outputs/
├── figures/     # gráficos e mapas gerados (não versionado)
└── tables/      # tabelas de resultado geradas (não versionado)
```

## Limitações já identificadas (para a seção de Metodologia do artigo)

- Nível 1 é um estudo **ecológico** (dados agregados por município, não
  individuais) — associação, não causalidade individual. O resultado sustenta
  "municípios com mais idosos sozinhos internam mais", não "o idoso que mora
  sozinho interna mais" (**falácia ecológica**).
- **A associação não é robusta à especificação do modelo** — ver a tabela de
  robustez acima e a seção 4.4 do notebook 04.
- `domicilios_resp_idoso` é o nº de domicílios com responsável idoso, não o
  nº total de idosos do município (um idoso que mora na casa de um filho, por
  exemplo, não é contado) — ver nota do notebook 01.
- As "causas" de internação são capítulos inteiros da CID-10 (o nível mais
  fino que o TabNet oferece), mais largos que os subgrupos do plano original
  (quedas, fratura de fêmur, síncope, confusão mental) — ver notebook 02 e
  `config.CAUSAS_SIH`. O capítulo V (transtornos mentais) é o mais largo:
  tratar como complementar, não como pilar do argumento.
- O recorte temporal do SIH é Jan/2022-Jul/2026 (últimos seis meses
  provisórios), não 2019-2022 como no plano original.
- O IDH cobre 259 dos 645 municípios, e é o IDHM 2010 (o Censo 2022 ainda não
  tem IDHM publicado) — depois da limpeza, a análise principal roda com n=250.
- **Rio Claro não é um caso extremo:** tem proporção de idosos sozinhos
  próxima da mediana estadual e taxa de internação *abaixo* da maioria dos
  municípios. O Nível 2 vale como caso com dado socioeconômico rico
  (CadÚnico), não como "município onde o problema é mais grave" — ver a nota
  na seção 5.1 do notebook 05.
- O CadÚnico (Nível 2) cobre apenas famílias de baixa renda — qualquer
  conclusão baseada nele vale para "idosos em situação de vulnerabilidade
  socioeconômica em Rio Claro", não para todos os idosos do município.
