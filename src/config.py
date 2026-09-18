"""Configurações e constantes compartilhadas pelos notebooks do pipeline.

Todos os notebooks importam este módulo (via `sys.path.append("../src")`)
para não duplicar caminhos de pasta, códigos de município e listas de CID-10
em cinco lugares diferentes.
"""
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
RIO_CLARO_CODIGO_IBGE = 3543907  # código IBGE de 7 dígitos de Rio Claro/SP
RIO_CLARO_NOME = "Rio Claro"

# O DATASUS costuma usar o código de município com 6 dígitos (o código IBGE
# de 7 dígitos sem o dígito verificador final). Guardamos os dois porque
# vamos precisar cruzar IBGE (7 dígitos) com DATASUS (6 dígitos) no notebook 03.
RIO_CLARO_CODIGO_DATASUS = str(RIO_CLARO_CODIGO_IBGE)[:6]  # "354390"


def codigo_ibge_para_datasus(codigo_ibge_7: int | str) -> str:
    """Converte um código IBGE de 7 dígitos no código de 6 dígitos usado pelo DATASUS
    (remove o último dígito, que é o dígito verificador)."""
    return str(codigo_ibge_7)[:6]

# ---------------------------------------------------------------------------
# Recorte temporal
# ---------------------------------------------------------------------------
ANOS_SIH = [2019, 2020, 2021, 2022]   # anos de internação a coletar no SIH/SUS
ANO_CENSO = 2022                       # ano do Censo Demográfico usado como referência

# Estatuto do Idoso (Lei 10.741/2003), art. 1º
IDADE_MINIMA_IDOSO = 60

# ---------------------------------------------------------------------------
# CID-10: causas de internação associadas à hipótese do estudo
# (quedas, confusão mental, fratura de fêmur e síncope são eventos que,
# na ausência de alguém por perto, tendem a ser percebidos e socorridos
# mais tarde — por isso são o foco da análise, e não "qualquer internação").
#
# Os prefixos abaixo são comparados com os 3 primeiros caracteres do campo
# DIAG_PRINC do SIH (diagnóstico principal, sem ponto, ex: "S720").
# ---------------------------------------------------------------------------
CAUSAS_CID10: dict[str, list[str]] = {
    "quedas": [f"W{i:02d}" for i in range(0, 20)],  # W00-W19 - Quedas (capítulo XX, causas externas)
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
    e devolve a categoria da causa conforme CAUSAS_CID10, ou 'outras'."""
    if not isinstance(cid, str) or not cid:
        return "outras"
    cid_limpo = cid.strip().upper().replace(".", "")
    for causa, prefixos in CAUSAS_CID10.items():
        if any(cid_limpo.startswith(p) for p in prefixos):
            return causa
    return "outras"
