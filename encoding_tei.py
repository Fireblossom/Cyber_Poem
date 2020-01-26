# encoding=utf-8
import json
import re
from verse_encoding import preprocess, metrics_analytics, METRICS
from xml.etree import ElementTree as ET
from xml.dom import minidom

def flatten(l):
    return [item for sublist in l for item in sublist]

def load_data():
    with open("data/rhymebooks.json") as output:
        rhymes = json.load(output)
    with open("data/TC2SC.json") as output:
        T2C = json.load(output)
    with open("data/kangxi.json") as output:
        Dict = json.load(output)
    with open("data/metric.name") as output:
        metric_names = [line.strip() for line in output]

    P_PING_unflattened = rhymes['平水韵'][0]
    Z_PING_unflattened = rhymes['平水韵'][1]
    P_PING = flatten(rhymes['平水韵'][0])
    Z_PING = flatten(rhymes['平水韵'][1])

    return rhymes, T2C, Dict, metric_names, P_PING_unflattened, Z_PING_unflattened, P_PING, Z_PING

def preprocess(raw):
    _, _, _, _, _, _, P_PING, Z_PING = load_data()
    clean = re.sub(r'[，。, .]', "", raw)
    tokens = [token for token in clean if token]
    tones  = []
    for t in tokens:
        if t in P_PING:
            if t in Z_PING:
                tones.append('1/0')
            else:
                tones.append('1')
        else:
            tones.append('0')
    return tokens,tones


def metricsAnalytics(verse, metrics):
    _, _, _, metric_names, P_PING_unflattened, _, _, _ = load_data()
    tokens, tones = verse
    print('五绝')
    count = 0
    RBOOK = P_PING_unflattened
    if tones[1] == '1':
        print('平起')
        metric = metrics[:2]
    else:
        print('仄起')
        metric = metrics[2:]

    for k, v in enumerate(RBOOK):
        if tokens[9] in v and tokens[19] in v:
            print("韵脚：", metric_names[k])
            if tones[4] == '1':
                num_metrics = 0
                if tokens[4] in v:
                    print('首句入韵')
            else:
                num_metrics = 1
                print('首句仄收，不入韵, 首句白脚')

                for k, (l1, l2) in enumerate(zip(tones, metric[num_metrics])):
                    if l1 == '1/0':
                        print("[检测到多音字", tokens[k], "]")
                    elif l2 == '1/0':
                        pass
                    elif l1 != l2 and k % 5 != 0:
                        if l1 == '0':
                            print(tokens[k], "失配,建议：仄")
                        else:
                            print(tokens[k], "失配,建议：平")
                        count += 1

    print('失配词数', count)

def xml_write(root, filepath):
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    raw_str = reparsed.toprettyxml(indent='', newl="")
    # print(raw_str)
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
    top_title.text = "格律诗三百首"
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

    text = ET.SubElement(TEI, "text")
    body = ET.SubElement(text, "body")
    top_lg = ET.SubElement(body, "lg")
    top_lg.attrib = {
        "type": "poem",
        "met": "met",
    }

    head = ET.SubElement(top_lg, "head")
    title = ET.SubElement(head, "title")
    # title.text = # 填诗名和作者进去
    for raw_verse in raw:
        verse = preprocess(raw_verse)
        analysis = metrics_analytics(verse, METRICS)
        text = ET.SubElement(TEI, "text")
        body = ET.SubElement(text, "body")
        top_lg = ET.SubElement(body, "lg")
        top_lg.attrib = {"type": "poem"}
        head = ET.SubElement(top_lg, "head")
        # title = ET.SubElement(head, "title")
        # title.text = analysis["title"] + "-" + analysis["author"]  # 填诗名和作者进去

    # tree = ET.ElementTree(TEI)
    # tree.write('output.xml' )
    xml_write(TEI,'output.xml')
    dom = minidom.parse('output.xml')  # or xml.dom.minidom.parseString(xml_string)
    print(dom.toprettyxml())
    return TEI
