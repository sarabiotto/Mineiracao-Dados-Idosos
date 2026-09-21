"""Configurações e constantes compartilhadas pelos notebooks do pipeline.

Todos os notebooks importam este módulo (via `sys.path.append("../src")`)
para não duplicar caminhos de pasta, códigos de município e listas de CID-10
em cinco lugares diferentes.
"""
import re
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos do projeto (funcionam independente de onde o notebook é aberto,
# desde que ele esteja dentro de notebooks/)
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_RAW = ROOT_DIR / "data" / "raw"                 # baixado automaticamente pelos notebooks
DATA_EXTERNAL = ROOT_DIR / "data" / "external"        # baixado manualmente por você (IDH, ESF, shapefile...)
DATA_PROCESSED = ROOT_DIR / "data" / "processed"      # gerado pelos próprios notebooks (saídas intermediárias e finais)
OUTPUTS_FIGURES = ROOT_DIR / "outputs" / "figures"
OUTPUTS_TABLES = ROOT_DIR / "outputs" / "tables"

for _dir in (DATA_RAW, DATA_EXTERNAL, DATA_PROCESSED, OUTPUTS_FIGURES, OUTPUTS_TABLES):
    _dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Identificação geográfica
# ---------------------------------------------------------------------------
UF_SIGLA = "SP"
UF_CODIGO_IBGE = 35            # código IBGE de 2 dígitos do estado de São Paulo
RIO_CLARO_CODIGO_IBGE = 3543907  # código IBGE de 7 dígitos de Rio Claro/SP (informativo/citação)
RIO_CLARO_CODIGO_DATASUS = str(RIO_CLARO_CODIGO_IBGE)[:6]  # "354390" (informativo/citação)
RIO_CLARO_NOME = "Rio Claro"


def codigo_ibge_para_datasus(codigo_ibge_7: int | str) -> str:
    """Converte um código IBGE de 7 dígitos no código de 6 dígitos usado pelo DATASUS
    (remove o último dígito, que é o dígito verificador)."""
    return str(codigo_ibge_7)[:6]

# ---------------------------------------------------------------------------
# Cruzamento de bases por NOME de município (não por código)
#
# Nenhuma das fontes reais que conseguimos (SIH/TabNet, Censo/SIDRA, IDH)
# traz o código IBGE de 7 dígitos diretamente utilizável entre si sem uma
# lista oficial de códigos — e não temos acesso à internet neste ambiente
# para baixar essa lista (API do IBGE). Por isso o pipeline cruza tudo pelo
# NOME do município, normalizado (maiúsculas, sem acento, sem sufixo "(SP)").
# Validado: todos os municípios do SIH batem com o Censo, exceto
# "SAO LUIS DO PARAITINGA", grafia alternativa de "São Luiz do Paraitinga",
# tratada em ALIASES_MUNICIPIO; e 259 de 260 do IDH (a exceção,
# "Guaxupé", nem é município de SP — é de MG, aparentemente um erro no
# arquivo de origem, e por isso fica de fora sem problema).
# ---------------------------------------------------------------------------
ALIASES_MUNICIPIO = {
    "SAO LUIS DO PARAITINGA": "SAO LUIZ DO PARAITINGA",
}


def normalizar_municipio(nome: str) -> str:
    """Normaliza um nome de município para cruzar bases de fontes diferentes:
    maiúsculas, sem acento, sem sufixo '(SP)', sem espaços duplicados."""
    if not isinstance(nome, str):
        return ""
    nome = nome.strip()
    nome = re.sub(r"\s*\(SP\)\s*$", "", nome, flags=re.IGNORECASE)
    nome = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("ascii")
    nome = nome.upper().strip()
    nome = re.sub(r"\s+", " ", nome)
    return ALIASES_MUNICIPIO.get(nome, nome)

# ---------------------------------------------------------------------------
# Recorte temporal
#
# O plano original era 2019-2022. Os dados reais do SIH que conseguimos via
# TabNet cobrem Jan/2022 a Jul/2026 (ver data/external/FONTES_RIO_CLARO.md) —
# o recorte mudou para acompanhar o dado disponível. Jul/2026 é o último mês
# publicado e os últimos seis meses são provisórios (sujeitos a atualização,
# conforme nota do próprio TabNet).
#
# Os exports trazem uma coluna por ano (TabNet com Coluna = "Ano
# processamento"). 2026 cobre só até julho, então entra nos gráficos de
# série temporal marcado como parcial e fica fora do ajuste de tendência.
# ---------------------------------------------------------------------------
PERIODO_SIH = "Jan/2022-Jul/2026"   # recorte coberto pelos exports do TabNet
ANOS_SIH = [2022, 2023, 2024, 2025, 2026]
ANO_SIH_PARCIAL = 2026              # só até julho -- não comparar de igual para igual com os anos cheios
ANO_CENSO = 2022                    # ano do Censo Demográfico usado como referência

# Estatuto do Idoso (Lei 10.741/2003), art. 1º
IDADE_MINIMA_IDOSO = 60

# ---------------------------------------------------------------------------
# Causas de internação associadas à hipótese do estudo — nível SIH/TabNet
#
# O TabNet do DATASUS exporta pelo filtro "Capítulo CID-10", não por
# subcategoria (não dá pra pedir só W00-W19 ou só S72 direto na interface).
# Por isso as 3 causas abaixo são capítulos inteiros da CID-10, uma
# aproximação mais larga do que os subgrupos que pretendíamos originalmente
# (quedas, fratura de fêmur, síncope, confusão mental) — declarar isso como
# limitação no artigo. Cada uma cobre o(s) subgrupo(s) de interesse, mas
# também internações que não são o foco:
#
# - lesoes_causas_externas (Cap. XIX): inclui quedas (W00-W19) e fratura de
#   fêmur (S72), mas também outras lesões/intoxicações não relacionadas.
# - sintomas_sinais_maldefinidos (Cap. XVIII): inclui síncope (R55) e
#   confusão mental (R41), mas também outros sintomas mal definidos — este
#   capítulo é inclusive usado na literatura de saúde pública como proxy de
#   diagnóstico tardio/impreciso, o que reforça (não enfraquece) a hipótese.
# - transtornos_mentais (Cap. V): inclui delirium (F05), mas é o mais largo
#   dos três — também cobre transtornos por uso de substâncias, esquizofrenia
#   etc., sem relação direta com isolamento. Considerar tratar como
#   complementar/exploratório, não como pilar central do argumento.
# ---------------------------------------------------------------------------
CAUSAS_SIH: dict[str, str] = {
    "lesoes_causas_externas": "Cap. XIX - Lesões e causas externas (quedas, fraturas etc.)",
    "sintomas_sinais_maldefinidos": "Cap. XVIII - Sintomas e sinais mal definidos (inclui síncope, confusão mental)",
    "transtornos_mentais": "Cap. V - Transtornos mentais e comportamentais (inclui delirium)",
}

CAUSAS_SIH_LABELS = {
    "lesoes_causas_externas": "Lesões e causas externas",
    "sintomas_sinais_maldefinidos": "Sintomas mal definidos",
    "transtornos_mentais": "Transtornos mentais",
}

# ---------------------------------------------------------------------------
# CID-10 por subcategoria — mantido para o caminho alternativo via pysus/AIH
# (microdados individuais), caso um dia se torne viável filtrar por
# subcategoria em vez de capítulo. Não é usado no caminho principal (TabNet).
# ---------------------------------------------------------------------------
CAUSAS_CID10: dict[str, list[str]] = {
    "quedas": [f"W{i:02d}" for i in range(0, 20)],  # W00-W19 - Quedas (capítulo XIX, causas externas)
    "fratura_femur": ["S72"],                         # S72.x - Fratura do fêmur
    "sincope": ["R55"],                                # R55 - Síncope e colapso
    "confusao_mental": ["R41", "F05"],                 # R41.x - Confusão mental / F05 - Delirium
}

CAUSAS_LABELS = {
    "quedas": "Quedas",
    "fratura_femur": "Fratura de fêmur",
    "sincope": "Síncope e colapso",
    "confusao_mental": "Confusão mental / delirium",
    "outras": "Outras causas",
}


def classificar_causa(cid: str) -> str:
    """Recebe um código CID-10 (com ou sem ponto, ex: 'S72.0' ou 'S720')
    e devolve a categoria da causa conforme CAUSAS_CID10, ou 'outras'.
    Usado apenas no caminho alternativo via microdados (pysus)."""
    if not isinstance(cid, str) or not cid:
        return "outras"
    cid_limpo = cid.strip().upper().replace(".", "")
    for causa, prefixos in CAUSAS_CID10.items():
        if any(cid_limpo.startswith(p) for p in prefixos):
            return causa
    return "outras"
