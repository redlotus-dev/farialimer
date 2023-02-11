"""Layout 00 Specification"""

from collections import namedtuple

NUMERIC = "numeric"
TEXT = "text"
DATE = "date"
Field = namedtuple("field", ["description", "datatype", "start", "end"])

layout = [
    Field("tipo_de_registro", TEXT, 1, 2),
    Field("codigo_do_arquivo", TEXT, 3, 11),
    Field("codigo_da_categoria_do_usuario", NUMERIC, 12, 14),
    Field("codigo_do_usuario", NUMERIC, 15, 21),
    Field("codigo_da_origem", TEXT, 22, 29),
    Field("codigo_do_destino", NUMERIC, 30, 44),
    Field("numero_do_movimento", NUMERIC, 45, 53),
    Field("data_da_geracao_do_arquivo", DATE, 54, 61),
    Field("data_do_movimento", DATE, 62, 69),
    Field("reserva", TEXT, 70, 1000),
]
