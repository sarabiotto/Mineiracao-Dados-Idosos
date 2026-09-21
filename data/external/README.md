# data/external/ — downloads manuais

Esta pasta guarda arquivos que **você precisa baixar manualmente** (não têm
API estável, ou o pipeline automático pode falhar). Os notebooks leem esses
arquivos daqui pelo nome exato indicado.

| Arquivo | Onde baixar | Usado no |
|---|---|---|
| `tabela9879_domicilios_sp.csv` | ✅ já temos — SIDRA, 645/645 municípios, Censo 2022 (ver `FONTES_RIO_CLARO.md`) | Notebook 01 (caminho principal, já testado) |
| `idh_sp.csv` | ✅ já temos (259 de 645 municípios úteis — ver `FONTES_RIO_CLARO.md`) | Notebook 03 |
| `cadunico_rio_claro.csv` | ✅ já temos — Ofício SMDS nº 2235/2026, Prefeitura de Rio Claro | Notebook 05, seção 5.4 |
| `censo_rio_claro_historico.csv` | ✅ já temos — mesmo ofício, população/idosos 1970-2022 | Notebook 05, seção 5.5 |
| `2026-09-14_..._FATEC_IA_assinado.pdf` | ✅ já temos — ofício original (fonte dos dois arquivos acima) | referência/citação |
| `sih_residencia_lesoes_sp.csv`, `sih_residencia_sintomas_sp.csv`, `sih_residencia_tmentais_sp.csv` | ✅ já temos — TabNet **por local de residência**, Jan/2022-Jul/2026, um por capítulo CID-10 (ver `FONTES_RIO_CLARO.md`) | Notebook 02 (caminho principal, já testado) |
| `sih_lesoes_sp.csv`, `sih_sintomas_sp.csv`, `sih_transtornos_mentais_sp.csv` | ⚠️ **superados** — mesma consulta, mas por local de **internação** (hospital). Mantidos só para a comparação documentada em `FONTES_RIO_CLARO.md` | nenhum notebook lê mais |
| `sp_municipios.zip` | https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/UFs/SP/SP_Municipios_2022.zip | Notebook 04 (mapa — opcional) |
| `esf_sp.csv` | https://egestorab.saude.gov.br → Cobertura AB → SP → 2022 → exportar CSV | Opcional — variável de controle adicional, ainda não usada nos notebooks |

**Pipeline completo e testado de ponta a ponta com dado real** — todos os
dados essenciais (Nível 1 e Nível 2) já estão aqui. `tabela9605_*.csv`
(a tabela errada, mantida só de referência histórica) pode ser apagada.

Os arquivos desta pasta não são versionados no Git (ver `.gitignore`), exceto
este README e o `FONTES_RIO_CLARO.md` — que documentam o que precisa estar
aqui e de onde veio cada arquivo, mesmo sem os dados em si estarem no
repositório.
