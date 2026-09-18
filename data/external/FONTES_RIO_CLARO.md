# Fontes dos dados de Rio Claro (Nível 2)

## `cadunico_rio_claro.csv` e `censo_rio_claro_historico.csv`

Extraídos do **Ofício SMDS nº 2235/2026**, da Seção de Vigilância
Socioassistencial (Secretaria Municipal de Desenvolvimento Social,
Prefeitura Municipal de Rio Claro-SP), de 14/09/2026, assinado digitalmente
por Marcel Giovane Martins Rodrigues (Líder de Seção), em resposta a
solicitação de dados para fins acadêmicos.

- **Tabela 1 do ofício** → `censo_rio_claro_historico.csv`: população total
  e pessoas idosas (60+) em Rio Claro, 1970-2022, conforme Censos IBGE.
- **Tabela 2 do ofício** → `cadunico_rio_claro.csv`: pessoas idosas no
  Cadastro Único de Rio Claro (dados de Junho/2026), por faixa de renda
  familiar per capita, com o total de idosos e quantos estão em famílias
  unipessoais (moram sozinhos) em cada faixa. **Dado agregado, sem
  identificação individual** — não há necessidade de aprovação de CEP para
  uso nesta forma.

Dados adicionais mencionados no ofício (ainda não incorporados a nenhuma
tabela, mas citáveis no artigo):
- BPC Idoso (65+): 2.130 beneficiários em Rio Claro (Julho/2026)
- Serviço de Convivência e Fortalecimento de Vínculos (SCFV): 231 pessoas
  idosas atendidas

**Limitação a declarar no artigo:** o Cadastro Único cobre apenas famílias
de baixa renda — os 8.439 idosos cadastrados representam ~22,8% do total de
idosos do município (37.038, Censo 2022). Qualquer conclusão da seção de
Rio Claro baseada no CadÚnico vale para "idosos em situação de
vulnerabilidade socioeconômica em Rio Claro", não para todos os idosos do
município.

O arquivo PDF original do ofício está em
`data/external/2026-09-14_Pessoas_Idosas_-_FATEC_IA_assinado.pdf` (guarde-o
localmente — não versionado no Git por conter dados enviados oficialmente à
FATEC, mesmo sendo agregado).

## `idh_sp.csv`

Fornecido por você (IDHM municipal, valores compatíveis com IDHM 2010 do
Atlas Brasil — ex.: São Caetano do Sul 0,862 bate com o valor oficial).

⚠️ **Cobertura parcial:** o arquivo tem apenas **260 dos 645 municípios de
SP**. Isso significa que, na análise estadual (Nível 1, notebook 04), ~385
municípios ficarão sem IDH e cairão fora da regressão que usa essa
variável como controle (ou entrarão com `NaN`, dependendo de como
`statsmodels` trata valores ausentes — por padrão, remove essas linhas).
Duas opções, para decidirmos juntas quando chegarmos nessa etapa:
1. Seguir só com os 260 municípios que têm IDH (amostra menor, mas válida)
2. Completar o arquivo baixando o restante do Atlas Brasil

## Tabela 9605 do SIDRA (`tabela9605_Rio_Claro.csv`, `tabela9605_s_o_Paulo.csv`)

**Não é a tabela certa para "idosos morando sozinhos".** Ela traz
"População residente, por cor ou raça" — só o total de população, sem
recorte de idade ou arranjo domiciliar — e por **Concentração Urbana** (uma
unidade geográfica do IBGE que agrupa municípios vizinhos), não por
município individual. Por isso o valor de Rio Claro nela (231.860) não bate
com a população do município isoladamente (201.418, conforme o ofício da
Prefeitura) — é a população de toda a aglomeração urbana.

Esses dois arquivos não foram incorporados ao pipeline. Ver próximos passos
no README principal sobre como achar a tabela certa (arranjo domiciliar
unipessoal por idade, nível município).
