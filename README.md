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
| DATASUS — SIH/SUS (TabNet) | Internações de idosos por capítulo CID-10, por município, 2022-2026 | 327/645 municípios com alguma internação registrada (os demais entram com 0) |
| Atlas Brasil | IDH municipal (controle) | 259/645 municípios |
| CadÚnico de Rio Claro (Ofício SMDS nº 2235/2026) | Renda, composição domiciliar (Nível 2) | Só Rio Claro, só famílias de baixa renda |

**Importante:** nenhuma dessas fontes trouxe o código IBGE de 7 dígitos
utilizável em conjunto com as outras, e não há acesso à internet neste
ambiente de desenvolvimento para baixar a lista oficial de códigos do IBGE.
Por isso todo o cruzamento entre bases é feito por **nome de município
normalizado** (`config.normalizar_municipio`) — validado com taxa de
correspondência muito alta (326/327 no SIH, 259/260 no IDH; ver
`FONTES_RIO_CLARO.md` para os casos que não bateram e por quê).

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
2. Abra o Jupyter:
   ```
   jupyter notebook
   ```
3. Rode os notebooks **em ordem**, dentro de `notebooks/`:

   | Notebook | O que faz | Saída |
   |---|---|---|
   | `01_coleta_ibge_censo.ipynb` | Idosos sozinhos por município (Censo 2022, tabela 9879) | `censo_domicilios_sp.csv` |
   | `02_coleta_datasus_sih.ipynb` | Internações de idosos por capítulo CID-10 (SIH/SUS) | `internacoes_sp.csv` |
   | `03_integracao_limpeza.ipynb` | Junta tudo por nome de município; gera painel, base agregada e base **limpa** (outliers e municípios sem IDH removidos) | `dataset_consolidado_sp.csv`, `dataset_municipios_sp_bruto.csv`, `dataset_municipios_sp.csv` |
   | `04_analise_estatistica.ipynb` | Correlação, regressão (nível município, n≈240 após limpeza), checagem de robustez, mapa opcional | figuras + `regressao_ols.txt` |
   | `05_estudo_caso_rio_claro.ipynb` | Comparação, projeção e perfil socioeconômico — Rio Claro | figuras |

Todos os arquivos de entrada já estão descritos em
[`data/external/README.md`](data/external/README.md).

## Dois pontos metodológicos importantes (notebook 03/04)

**Pseudorreplicação:** `pct_idosos_sozinhos` vem do Censo 2022 — é
**constante ao longo dos 5 anos** de cada município. Testar a hipótese no
painel (3.225 linhas, 5 por município) infla o "n" artificialmente
([pseudorreplicação](https://en.wikipedia.org/wiki/Pseudoreplication)). Por
isso a hipótese é testada na base por município (uma linha por município) —
o painel serve só para gráficos de evolução temporal.

**Limpeza (notebook 03, seção 3.5):** a base por município passa por três
tratamentos antes de virar `dataset_municipios_sp.csv`:
1. Arredondamento das taxas (2 casas decimais — sem perda de informação real)
2. Remoção de outliers na taxa de internação pela regra de Tukey (acima de
   Q3 + 1,5×IQR) — 19 municípios. Não é ruído aleatório: os removidos são,
   em maioria, cidades-polo regionais em saúde (Presidente Prudente,
   Botucatu, Jaú...), consistente com a suspeita de que o SIH que temos é
   "por local de internação" (hospital), não "por local de residência"
   (paciente) — ver `FONTES_RIO_CLARO.md`.
3. Remoção de municípios sem IDH (377) — decisão de eliminar em vez de
   imputar, já que ~60% da coluna está ausente e não há fonte confiável de
   IDH por município vizinho disponível aqui para imputar com critério.

Isso reduz a base de 645 para **240 municípios**. A versão sem esses
filtros fica salva em `dataset_municipios_sp_bruto.csv`, e o notebook 04
(seção 4.2b) compara os resultados com e sem a limpeza como checagem de
robustez — o resultado muda de forma relevante (ver seção de Resultados),
o que é em si um achado sobre a qualidade do dado disponível.

## Como trabalhar nisso comigo

O pipeline já roda de ponta a ponta com o dado que temos — mas ainda dá pra
melhorar (completar o IDH para os ~386 municípios que faltam, por exemplo).
Se rodar um notebook e algo sair diferente do esperado, me manda a mensagem
completa (ou o que apareceu na tela) que eu ajusto com base nisso.

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
  individuais) — associação, não causalidade individual.
- `domicilios_resp_idoso` é o nº de domicílios com responsável idoso, não o
  nº total de idosos do município (um idoso que mora na casa de um
  filho, por exemplo, não é contado) — ver nota do notebook 01.
- As "causas" de internação são capítulos inteiros da CID-10 (o nível mais
  fino que o TabNet oferece), mais largos que os subgrupos do plano
  original (quedas, fratura de fêmur, síncope, confusão mental) — ver
  notebook 02 e `config.CAUSAS_SIH`.
- O recorte temporal do SIH é 2022-2026 (2026 parcial, até julho), não
  2019-2022 como no plano original — mudou para acompanhar o dado real
  disponível.
- O IDH cobre 259 dos 645 municípios — depois da limpeza (outliers + IDH
  ausente), a análise principal roda com n≈240.
- O IDH usado é o mais recente disponível fornecido (IDHM 2010, Atlas
  Brasil) — o Censo 2022 ainda não tem IDHM oficial publicado.
- **Resultado principal, honesto:** na base limpa, nem a correlação simples
  nem o coeficiente de `pct_idosos_sozinhos` na regressão são
  estatisticamente significativos (ver notebook 04, seção 4.3). O achado
  "quase significativo" que aparecia na base bruta não se sustenta depois
  da limpeza — reportar os dois resultados (bruto e limpo) no artigo como
  checagem de robustez, não só o mais favorável.
- O CadÚnico (Nível 2, Rio Claro) cobre apenas famílias de baixa renda —
  qualquer conclusão baseada nele vale para "idosos em situação de
  vulnerabilidade socioeconômica em Rio Claro", não para todos os idosos do
  município.
