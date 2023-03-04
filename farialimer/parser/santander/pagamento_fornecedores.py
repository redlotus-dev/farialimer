"""Parse module"""
from collections import namedtuple

from farialimer.parser.santander.base_santander import SantanderParser

Type3 = namedtuple("Type3", ["line", "register_type", "segment", "register_group"])

_identifier_map = {
    "01": "1CRE",
    "03": "1CRE",
    "05": "1CRE",
    "10": "1CRE",
    "20": "1CRE",
    "11": "1TRC",
    "16": "1TRS",
    "17": "1TRS",
    "22": "1TRS",
    "23": "1TRS",
    "24": "1TRS",
    "25": "1TRS",
    "26": "1TRS",
    "27": "1TRS",
    "30": "1TIT",
    "31": "1TIT",
    "35": "1OCT",
    "45": "1PIX",
}


class PagamentoFornecedoresParser(SantanderParser):
    """Read, parse and write"""

    def __init__(self, provider):
        super().__init__(provider=provider)
        self.current_register_header = None

    def get_line_register(self, line: str):
        """
            If the register type == 1,
            then an additional identifier type must be added to the register type.
            Identifier is at Position 12-13 (index=[11:13]).
            if identifier in (01, 03, 05, 10, 20), then register type is 1CRE
            if identifier in (11), then register type is 1TRC
            if identifier in (16, 17, 22, 23, 24, 25, 26, 27), then register type is 1TRS
            if identifier in (30, 31), then register type is 1TIT
            if identifier in (35), then register type is 1OCT
            if identifier in (45), then register type is 1PIX

            an outlier is the captura de titulos, where the op_type is at position 09 (index=[08]),
            if op_type == "I" then register type is 1CAP

        If the register type == 3,
            then an additional segment type must be added to the register type.
            based on the batch header record (type = 1)

            Segment is at Position 14 (index=13)
            If segment == J, another additional identifier type must be added to the register type.
            if the position 18-19 == 52, then register type is 3J52, else its 3J

            if the segment == N, an additional identifier type must be added to the register type.
            it's located at position 133-134 (index=[132-133])

            if the segment == W, an additional identifier type must be added to the register type.
            it´s located at position 177-178 (index=[176-177])

        if the register type == 5,
            then an additional identifier type must be added to the register type.

        registers type 0 and 9 are the same for all services
        """

        register_type = line[7]
        operation_type = line[8]

        try:
            if register_type == "1":
                return self._get_register_type_1(line, operation_type)
            if register_type == "3":
                return self._get_register_type_3(line, register_type)
            return register_type + self.current_register_header[1:]
        except TypeError as err:
            print(line)
            raise TypeError from err

    def _get_register_type_1(self, line, operation_type):
        """Return the register type 1"""
        if operation_type == "I":
            identifier = "1CAP"
        else:
            identifier_code = line[11:13]
            identifier = _identifier_map[identifier_code]
        self.current_register_header = identifier
        return self.current_register_header

    def _get_register_type_3(self, line, register_type):
        segment = line[13]
        register_group = self.current_register_header[1:]
        args = Type3(line, register_type, segment, register_group)
        _type_3_map = {
            "J": _get_segment_j,
            "N": _get_segment_n,
            "W": _get_segment_w,
            "Y": _get_segment_y,
        }
        func_method = _type_3_map.get(segment, _default_segment)
        return func_method(args)


def _default_segment(args: Type3):
    return args.register_type + args.segment + args.register_group


def _get_segment_y(args: Type3):
    segment = args.segment
    if args.line[17:19] == "53":
        segment += "53"
    return args.register_type + segment + args.register_group


def _get_segment_w(args):
    identifier = args.line[176:178]
    segment = args.segment
    if identifier == "01":
        segment += "1"
    return args.register_type + segment + args.register_group


def _get_segment_n(args: Type3):
    identifier = args.line[132:134]
    segment = args.segment
    _n_map = {
        "17": "1",
        "16": "2",
        "22": "4",
        "23": "4",
        "24": "4",
        "25": "5",
        "27": "6",
        "26": "7",
    }
    return args.register_type + segment + _n_map[identifier] + args.register_group


def _get_segment_j(args: Type3):
    identifier = args.line[17:19]
    if identifier == "52":
        return args.register_type + args.segment + identifier + args.register_group
    return args.register_type + args.segment + args.register_group
