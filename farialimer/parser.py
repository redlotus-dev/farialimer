import farialimer.providers.b3.documents.imbarq014.layouts as layout


class Parser:
    @staticmethod
    def read_file(filepath):
        with open(filepath) as finput:
            content = finput.readlines()
        return content

    def parse_content(self, content):
        filetype = get_filetype(content[0])  # primeira linha do conteudo
        print(filetype)
        for line in content:
            line_register = self._get_line_register(line)
            layout = self._get_layout(line_register)
            print(filetype, line_register, layout)
        # qual é o tipo de arquivo
        # qual é o layout

    def write(self, filteype):
        pass

    def _get_line_register(self, line: str):
        return line[:2]

    def _get_layout(self, line_register: str):
        _register_map = {
            "00": layout.layout_00,
            "18": layout.layout_18,
            "19": layout.layout_19,
            "31": layout.layout_31,
            "99": layout.layout_99,
        }
        return _register_map[line_register]


def get_filetype(line):
    return line[2:11]
