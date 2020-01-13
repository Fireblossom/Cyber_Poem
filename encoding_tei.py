from verse_encoding import *
from xml.etree import ElementTree as ET
from xml.dom import minidom


def tei_write(root, filepath):
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    raw_str = reparsed.toprettyxml(indent='', newl="")
    file = open(filepath, 'w', encoding='utf-8')
    file.write('<?xml version="1.0" encoding="UTF-8"?>')
    file.write(raw_str)
    file.close()


def build_tei_object(raw):
    verse = preprocess(raw)
    metrics_analytics(verse, metrics)

    # Following https://teibyexample.org/examples/TBED04v00.htm
    TEI = ET.Element("TEI")
    TEI.attrib = {"xmlns": "http://www.tei-c.org/ns/1.0"}

    teiHeader = ET.SubElement(TEI, "teiHeader")
    encodingDesc = ET.SubElement(teiHeader, "encodingDesc")
    metDecl = ET.SubElement(encodingDesc, "metDecl")
    metDecl.attrib = {}
    # 填格律进去

    text = ET.SubElement(TEI, "text")
    body = ET.SubElement(text, "body")
    top_lg = ET.SubElement(body, "lg")
    top_lg.attrib = {
        "type": "poem",
        "met": metrics,
    }
    head = ET.SubElement(top_lg, "head")
    title = ET.SubElement(head, "title")
    # title.text = # 填诗名进去

    return TEI

