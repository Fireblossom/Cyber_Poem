from verse_encoding import preprocess, metrics_analytics, METRICS
from xml.etree import ElementTree as ET
from xml.dom import minidom


def xml_write(root, filepath):
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    raw_str = reparsed.toprettyxml(indent='', newl="")
    file = open(filepath, 'w', encoding='utf-8')
    file.write('<?xml version="1.0" encoding="UTF-8"?>')
    file.write(raw_str)
    file.close()


def build_tei_object(raw):
    """
    :param raw: List of raw verses.
    :return: TEI: ElementTree object.
    """
    #  Following https://teibyexample.org/examples/TBED04v00.htm
    TEI = ET.Element("TEI")
    TEI.attrib = {"xmlns": "http://www.tei-c.org/ns/1.0"}

    teiHeader = ET.SubElement(TEI, "teiHeader")
    fileDesc = ET.SubElement(teiHeader, "fileDesc")
    titleStmt = ET.SubElement(fileDesc, "titleStmt")
    top_title = ET.SubElement(titleStmt, "title")
    top_title.text = "格律诗三（）百首"
    publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
    top_p = ET.SubElement(publicationStmt, "p")
    top_p.text = "Text Technology"
    sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
    top_p = ET.SubElement(sourceDesc, "p")
    top_p.text = "Wiki"

    encodingDesc = ET.SubElement(teiHeader, "encodingDesc")
    metDecl = ET.SubElement(encodingDesc, "metDecl")
    metDecl.attrib = {"pattern": "((+|-)+\|?/?)*"}  # 填格律进去
    metSym = ET.SubElement(metDecl, "metSym")  # 平
    metSym.attrib = {"value": "+"}
    metSym.text = "metrical promimence"
    metSym = ET.SubElement(metDecl, "metSym")  # 仄
    metSym.attrib = {"value": "-"}
    metSym.text = "metrical non-promimence"
    metSym = ET.SubElement(metDecl, "metSym")  # 中
    metSym.attrib = {"value": "~"}
    metSym.text = "metrical promimence or non-promimence"
    metSym = ET.SubElement(metDecl, "metSym")  # 音部
    metSym.attrib = {"value": "｜"}
    metSym.text = "foot boundary"
    metSym = ET.SubElement(metDecl, "metSym")  # 格律
    metSym.attrib = {"value": "/"}
    metSym.text = "metrical line boundary"

    for raw_verse in raw:
        verse = preprocess(raw_verse)
        analysis = metrics_analytics(verse, METRICS)
        text = ET.SubElement(TEI, "text")
        body = ET.SubElement(text, "body")
        top_lg = ET.SubElement(body, "lg")
        top_lg.attrib = {"type": "poem"}

        head = ET.SubElement(top_lg, "head")
        title = ET.SubElement(head, "title")
        title.text = analysis["title"] + "-" + analysis["author"]  # 填诗名和作者进去
    return TEI
