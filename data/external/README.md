# data/external/ — downloads manuais

Esta pasta guarda arquivos que **você precisa baixar manualmente** (não têm
API estável, ou o pipeline automático pode falhar). Os notebooks leem esses
arquivos daqui pelo nome exato indicado.

| Arquivo | Onde baixar | Usado no |
|---|---|---|
| `censo_domicilios_sp.csv` | https://sidra.ibge.gov.br/tabela/9605 (Município = SP) | Notebook 01 — só é necessário se a tentativa automática pela API SIDRA falhar |
| `idh_sp.xlsx` | http://www.atlasbrasil.org.br/ranking (Estado = SP → baixar Excel) | Notebook 03 |
| `sp_municipios.zip` | https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/UFs/SP/SP_Municipios_2022.zip | Notebook 04 (mapa — opcional) |
| `esf_sp.csv` | https://egestorab.saude.gov.br → Cobertura AB → SP → 2022 → exportar CSV | Opcional — variável de controle adicional, ainda não usada nos notebooks |
| `sih_sp_manual_*.csv` | http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/mrsp.def | Notebook 02 — só é necessário se a biblioteca `pysus` falhar |
| `cadunico_rio_claro.*` | Prefeitura de Rio Claro / CRAS / CECAD (quando disponível) | Notebook 05, seção 5.4 (ainda não integrado) |

Os arquivos desta pasta não são versionados no Git (ver `.gitignore`) porque
alguns são grandes e/ou podem ter restrições de uso — mas esta lista sim,
para todo mundo saber o que precisa baixar para rodar o projeto do zero.
