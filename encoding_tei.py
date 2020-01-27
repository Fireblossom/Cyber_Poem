# encoding=utf-8
import json
import re
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

def preprocess(filename):
    _, _, _, _, _, _, P_PING, Z_PING = load_data()
    with open(filename) as op:
        lines = op.readlines()
    lines = [re.sub(r'[，。, .]', "", line.strip()) for line in lines]
    title = lines[0]
    signed = lines[1]
    verse = lines[2:]
    tokens = [token for token in flatten(verse) if token]
    tones  = []
    for t in tokens:
        if t in P_PING:
            if t in Z_PING:
                tones.append('1/0')
            else:
                tones.append('1')
        else:
            tones.append('0')
    return tokens,tones,title,signed,verse

def xml_write(root, filepath):
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    raw_str = reparsed.toprettyxml(indent='', newl="")
    # print(raw_str)
    file = open(filepath, 'w', encoding='utf-8')
    file.write('<?xml version="1.0" encoding="UTF-8"?>')
    file.write(raw_str)
    file.close()


def metricsAnalytics(tokens, tones, metrics):
    _, _, _, metric_names, P_PING_unflattened, _, _, _ = load_data()
    #     tokenstonees = verse
    met_type = ""
    met_type += '五绝'
    count = 0
    met = []
    met_real = []
    RBOOK = P_PING_unflattened
    if tones[1] == '1':
        met_type += '平起'
        metric = metrics[:2]
    else:
        met_type += '仄起'
        metric = metrics[2:]

    for k, v in enumerate(RBOOK):
        if tokens[9] in v and tokens[19] in v:
            if tones[4] == '1':
                num_metrics = 0
                met_type += '首句入韵'
                rhyme = "aaba"
            else:
                num_metrics = 1
                met_type += '首句不入韵'
                rhyme = "abcb"

            for k, (l1, l2) in enumerate(zip(tones, metric[num_metrics])):
                #                     met = metric[num_metrics]
                if l1 == '1/0':
                    pass
                #               print("[检测到多音字",tokens[k],"]")
                elif l2 == '1/0':
                    pass
                elif l1 != l2 and k % 5 != 0:
                    if l1 == '0':
                        pass
                    #                         print(tokens[k],"失配,建议：仄")
                    else:
                        pass
                    #                         print(tokens[k],"失配,建议：平")
                    count += 1

    for m in metric[num_metrics]:
        if m == '1':
            met.append('+')
        else:
            met.append('-')

    for k, v in enumerate(tones):
        if v == metric[num_metrics][k] or v == '1/0':
            met_real.append(met[k])
        else:
            met_real.append('+' if v == '1' else '-')
    return met_type, met, met_real, rhyme


def build_tei_object(filenames, metrics):
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

    for fn in filenames:
        lg = ET.SubElement(top_lg, "lg")
        lg.attrib = {
            "type": "poem",
        }
        Tokens, Tones, Title, Signed, Verse = preprocess(fn)
        Met_type, Met, Met_real, Rhyme = metricsAnalytics(Tokens, Tones, metrics)
        head = ET.SubElement(lg, "head")
        title = ET.SubElement(head, "title")
        title.text = Title
        llg = ET.SubElement(lg, "lg")
        llg.attrib = {
            "type": Met_type,
            "rhyme": Rhyme
        }
        for i, line in enumerate(Verse):
            l = ET.SubElement(llg, "l")
            met = Met[0 + 5 * i:5 + 5 * i]
            real_met = Met_real[0 + 5 * i:5 + 5 * i]
            if met != real_met:
                l.attrib = {
                    "met": ''.join(met),
                    "real": ''.join(real_met),
                    "rhyme": Rhyme[i]
                }
            else:
                l.attrib = {
                    "met": ''.join(met),
                    "rhyme": Rhyme[i]
                }

            l.text = line[:-1]
            rrhyme = ET.SubElement(l, "rhyme")
            rrhyme.text = line[-1]

        signed = ET.SubElement(lg, "signed")
        signed.text = Signed

    rough_string = ET.tostring(TEI, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    #     mydata = ET.tostring(data)
    #     myfile = open("items2.xml", "w")
    #     myfile.write(mydata)
    with open('output.xml', "w") as output:
        output.write(reparsed.toprettyxml(indent="\t"))
    print(reparsed.toprettyxml(indent="\t"))

    return TEI
