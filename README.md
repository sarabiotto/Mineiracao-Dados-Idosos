# Mineiração de Dados — Idosos que moram sozinhos e internações evitáveis

Pesquisa que cruza bases públicas de saúde para investigar se idosos que
moram sozinhos são internados com mais frequência — e por causas mais
evitáveis (quedas, fratura de fêmur, síncope, confusão mental) — do que
idosos que não moram sozinhos.

**Hipótese:** quando um idoso mora sozinho, um evento como uma queda ou uma
confusão mental demora mais para ser percebido e socorrido, o que leva a
internações mais frequentes e por causas que uma presença humana por perto
poderia ter prevenido ou atenuado.

## Estrutura do estudo (dois níveis)

- **Nível 1 — Estado de São Paulo** (645 municípios): estudo ecológico,
  cruzando IBGE (Censo 2022) e DATASUS (SIH/SUS), com o IDH municipal como
  controle. Dá força estatística para publicação.
- **Nível 2 — Rio Claro**: estudo de caso aprofundado. Quando o CadÚnico do
  município estiver disponível, adiciona um recorte individual (renda,
  composição domiciliar, bairro) a este nível.

## Fontes de dados

| Fonte | O que fornece | Coleta |
|---|---|---|
| IBGE — Censo 2022 (SIDRA) | Idosos morando sozinhos por município | Automática (API), com caminho manual de apoio |
| DATASUS — SIH/SUS | Internações de idosos por causa (CID-10), por município | Automática (`pysus`), com caminho manual (TabNet) de apoio |
| Atlas Brasil | IDH municipal (controle) | Manual |
| CadÚnico de Rio Claro | Renda, composição domiciliar individual (Nível 2) | Em obtenção junto à Prefeitura/CRAS — ainda não integrado |

## Como rodar

1. Instale as dependências (Anaconda Prompt, na raiz do projeto):
   ```
   pip install -r requirements.txt
   ```
   Se `geopandas` falhar pelo pip, instale via conda:
   ```
   conda install -c conda-forge geopandas
   ```
2. Abra o Jupyter:
   ```
   jupyter notebook
   ```
3. Rode os notebooks **em ordem**, dentro de `notebooks/`:

   | Notebook | O que faz | Depende de |
   |---|---|---|
   | `01_coleta_ibge_censo.ipynb` | Idosos sozinhos por município (Censo 2022) | — |
   | `02_coleta_datasus_sih.ipynb` | Internações de idosos por causa (SIH/SUS) | — (mais demorado) |
   | `03_integracao_limpeza.ipynb` | Junta tudo em uma base só, por município/ano | Notebooks 01 e 02 |
   | `04_analise_estatistica.ipynb` | Correlação, regressão, mapa — nível estadual | Notebook 03 |
   | `05_estudo_caso_rio_claro.ipynb` | Comparação e projeção — Rio Claro | Notebook 03 |

Alguns arquivos precisam ser baixados manualmente antes de rodar certos
notebooks — a lista completa e onde baixar está em
[`data/external/README.md`](data/external/README.md).

## Como trabalhar nisso comigo

Os notebooks 01 e 02 têm partes marcadas como "a confirmar juntas" — a API
do SIDRA e a biblioteca `pysus` têm pontos que só validamos rodando de
verdade. **Rode célula por célula e, no primeiro erro ou resultado
inesperado, me manda a mensagem completa (ou o que apareceu na tela)** —
ajusto o código com base nisso em vez de adivinhar de antemão.

## Estrutura de pastas

```
data/
├── raw/         # baixado automaticamente pelos notebooks (não versionado)
├── external/    # baixado manualmente por você (não versionado, exceto o README)
└── processed/   # gerado pelos notebooks — dataset consolidado (não versionado)
notebooks/       # os 5 notebooks, na ordem de execução
src/config.py    # constantes e caminhos compartilhados pelos notebooks
outputs/
├── figures/     # gráficos e mapas gerados (não versionado)
└── tables/      # tabelas de resultado geradas (não versionado)
```

## Limitações já identificadas (para a seção de Metodologia do artigo)

- Nível 1 é um estudo **ecológico** (dados agregados por município, não
  individuais) — associação, não causalidade individual.
- O IDH municipal usado como controle é o mais recente disponível no Atlas
  Brasil; se o Censo 2022 ainda não tiver IDHM oficial publicado, o de 2010
  é usado como proxy.
- O CadÚnico (Nível 2, Rio Claro) cobre apenas famílias de baixa renda —
  qualquer conclusão do Nível 2 vale para "idosos em situação de
  vulnerabilidade socioeconômica em Rio Claro", não para todos os idosos do
  município.
