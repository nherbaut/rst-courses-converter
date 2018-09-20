import os
import lxml.etree as ET
from functools import reduce
import logging
import pkg_resources

ns = ET.FunctionNamespace("http://nextnet.top/functions")
ns.prefix = "nn"


class FileResolver(ET.Resolver):
    def resolve(self, url, pubid, context):
        return self.resolve_filename(url, context)


@ns
def urlencode(context, url):
    try:
        return url[0].replace("(", "%28").replace(")", "%29")
    except:
        logging.warning("failed to url encode url %s" % url)
        return url


XSLT_DIR = pkg_resources.resource_filename("rst_courses_converter", "xslt")
NO_SKIPPING = lambda x, y: False


class MDWriter:

    def __init__(self, infile):
        self.infile = infile
        self.output = ""

    def add_segment_code(self, segment):
        self.output += segment

    def parse_and_dump(self, outfile):
        # result concatenated here as text
        section_level = 0

        # load xslt files from folder and fillup transformers
        _, _, xslt_files = list(os.walk(XSLT_DIR))[0]
        xslt_transformers = {}
        for xslt_file in xslt_files:
            with open(os.path.join(XSLT_DIR, xslt_file), "r") as f:
                xslt_transformers[os.path.splitext(xslt_file)[0]] = ET.XSLT(ET.XML(f.read()))

        # load code transformers when xslt is too hard

        code_transformers = {}
        code_transformers["table"] = self.handle_table
        code_transformers["compound"] = self.handle_compound

        skipping = NO_SKIPPING

        for event, elem in ET.iterparse(self.infile, events=("start", "end")):

            tag = elem.tag
            if not skipping(tag, event):
                logging.debug("processing  %s %s " % (tag, event))
                if skipping != NO_SKIPPING:
                    skipping = NO_SKIPPING
                    logging.debug("not skipping anymore!")

                if event == "start":
                    if tag == "section":
                        section_level = section_level + 1
                    elif tag == "title":
                        self.add_segment_text("%s %s %s \n" % ("#" * section_level, elem.text, "#" * section_level))
                    elif tag in code_transformers:
                        skipping = MDWriter.__get_skipper(tag, "end")
                        self.add_segment_text("\n\n%s\n\n" % str(code_transformers[tag](elem)))
                    elif tag in xslt_transformers:
                        skipping = MDWriter.__get_skipper(tag, "end")
                        ze_xml = MDWriter.__clean_xml(ET.tostring(elem).decode("utf-8").replace("\n", " "))
                        self.add_segment_text("\n\n%s\n\n" % str(xslt_transformers[tag](ET.XML(ze_xml))))

                    elif tag == "literal_block":
                        skipping = MDWriter.__get_skipper(tag, "end")
                        self.add_segment_code(self.handle_literal_block(elem))
                    elif tag in ["document"]:
                        pass
                    else:
                        logging.debug("unknown tag " + tag)
                elif event == "end":
                    if tag == "section":
                        section_level = section_level - 1
            else:
                logging.debug("skipped  %s %s " % (tag, event))

        self.dump(outfile)

    def dump(self, filename):
        print("writing in %s" % filename)
        with open(filename, "w+") as f:
            f.write(self.output)

    @classmethod
    def __get_skipper(cls, skipping_tag, skipping_event):
        '''
        closure generator for tag /event skipping function
        :param skipping_tag:
        :param skipping_event:
        :return: a function that returns False while skipping_tag skipping_event are not seen
        '''
        logging.debug("--> skipping unil %s %s \n " % (skipping_tag, skipping_event))

        def skip(tag, event):
            if skipping_tag == tag and skipping_event == event:
                return False
            else:
                return True

        return skip

    @classmethod
    def __clean_xml(cls, paragraph_text):
        '''
        various hacky xml cleanup
        :param paragraph_text: str to clean
        :return: cleaned str
        '''
        if paragraph_text is None:
            return None

        paragraph_text = paragraph_text.replace("\n", " ")
        # remove repeated spaces
        output = reduce(lambda x, y: x if x[-1] == ' ' and y == ' ' else x + y, paragraph_text)
        return output

    def handle_literal_block(self, elem):
        '''
        apply specify treatment for code element
        :param elem: and xml element
        :return: MD representation for code
        '''
        language = elem.attrib.get("language", "text")
        code = elem.xpath('./text()')

        output = '''```%s\n\n%s\n```\n\n''' % (language, ''.join(code))
        return output

    def handle_compound(self, elem):
        output = ""
        tree = ET.XML(ET.tostring(elem))
        title = tree.xpath("//compound/compact_paragraph/caption/text()")
        if (len(title) > 0):
            title = title[0]
        if len(title)>0:
            output += "**%s**\n\n" % title

        for item in tree.xpath("//compound/compact_paragraph/bullet_list/list_item"):
            ref = item.xpath("./compact_paragraph/reference")[0]
            output += "* [%s](%s.%s)  \n" % (ref.xpath("./text()")[0], ref.xpath("./@refuri")[0],self.get_file_extension())

        return output

    def get_file_extension(self):
        return "md"
    def handle_table(self, elem):
        output = ""

        tree = ET.XML(ET.tostring(elem))
        title = tree.xpath("/table/title/text()")
        if (len(title) >= 1):
            title = title[0]
            output += "**%s**\n\n" % title



        # we don't support formatting within a table, so each entry's text is taken, concat and stipped

        headers = ["".join(entry.xpath(".//text()")).strip() for entry in tree.xpath("/table/tgroup/thead/row/entry")]
        output += "|%s|\n" % "|".join(headers)
        output += "|%s|\n" % "|".join(["---"] * len(headers))
        # now do the same thing with rows
        for row in tree.xpath("/table/tgroup/tbody/row"):
            row_entries_text = ["".join(entry.xpath(".//text()")).strip().replace("\n","\\") for entry in
                                row.xpath("./entry")]
            output += "|%s|\n" % "|".join(row_entries_text)
        return output

    def add_segment_code(self, segment):
        self.output += segment

    def add_segment_text(self, segment):
        self.output += segment
