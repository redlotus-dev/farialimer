from collections import namedtuple

NUMERIC = "numeric"
TEXT = "text"
DATE = "date"
field = namedtuple("field", ["description", "datatype", "start", "end"])

layout = [
    field("tipo_de_registro", TEXT, 1, 2),
    field("codigo_do_arquivo", TEXT, 3, 11),
    field("codigo_da_categoria_do_usuario", NUMERIC, 12, 14),
    field("codigo_do_usuario", NUMERIC, 15, 21),
    field("codigo_da_origem", TEXT, 22, 29),
    field("codigo_do_destino", NUMERIC, 30, 44),
    field("numero_do_movimento", NUMERIC, 45, 53),
    field("data_da_geracao_do_arquivo", DATE, 54, 61),
    field("data_do_movimento", DATE, 62, 69),
    field("reserva", TEXT, 70, 1000),
]
