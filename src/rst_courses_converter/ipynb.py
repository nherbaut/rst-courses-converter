from .md import MDWriter
import nbformat as nbf


class IPyNB(MDWriter):

    def __init__(self, infile):
        self.infile = infile
        self.output = ""
        self.nb = nbf.v4.new_notebook()
        self.nb["metadata"] = {"kernelspec": {
            "display_name": "Java",
            "language": "java",
            "name": "java"},
            "language_info": {
                "codemirror_mode": "java",
                "file_extension": ".java",
                "mimetype": "text/x-java-source",
                "name": "Java",
                "pygments_lexer": "java",
                "version": "10.0.2+13"}}

    def get_file_extension(self):
        return "ipynb"

    def handle_literal_block(self, elem):
        '''
        apply specify treatment for code element
        :param elem: and xml element
        :return: code representation for code
        '''

        code = elem.xpath('./text()')
        language = elem.attrib.get("language", "text")
        output = '%s' % (''.join(code))
        return (output, language)

    def add_segment_code(self, segment):
        code, language = segment

        if language == "java":
            cell = nbf.v4.new_code_cell(code)
        else:
            cell = nbf.v4.new_raw_cell(code)
        self.nb['cells'].append(cell)

    def add_segment_text(self, segment):
        cell = nbf.v4.new_markdown_cell(segment)
        self.nb['cells'].append(cell)

    def dump(self, filename):
        nbf.write(self.nb, filename)
