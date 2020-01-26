# encoding=utf-8
from encoding_tei import preprocess, metricsAnalytics, build_tei_object

raw1 = "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。"
raw2 = "迟日江山丽，春风花草香。泥融飞燕子， 沙暖睡鸳鸯。"
raw3 = "鸣筝金粟柱, 素手玉房前, 欲得周郎顾, 时时误拂弦"
raw4 = "花明绮陌春，柳拂御沟新。为报辽阳客，流芳不待人。"
raw5 = "北斗七星高，哥舒夜带刀。至今窥牧马，不敢过临洮。"
raw6 = "离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。"
raw7 = "泠泠七弦上，静听松风寒。古调虽自爱，今人多不弹。"
raw8 = "床前明月光，疑是地上霜。举头望明月，低头思故乡"

metrics = []

# 五绝平起首句入韵
metrics.append([
    '1','1','1/0','0','1',
    '1/0','0','0','1','1',
    '1/0','0','1','1','0',
    '1','1','1/0','0','1'])
# 五绝平起首句不入韵
metrics.append([
    '1/0','1','1','0','0',
    '1/0','0','0','1','1',
    '1/0','0','1','1','0',
    '1','1','1/0','0','1'])
# 五绝仄起首句入韵
metrics.append([
    '1/0','0','0','1','1',
    '1','1','1/0','0','1',
    '1/0','1','1','0','0',
    '1/0','0','0','1','1'])
# 五绝仄起首句不入韵
metrics.append([
    '1/0','0','1','1','0',
    '1','1','1/0','0','1',
    '1/0','1','1','0','0',
    '1/0','0','0','1','1'])

# verse1 = preprocess(raw1)
# verse2 = preprocess(raw2)
# verse3 = preprocess(raw3)
# verse4 = preprocess(raw4)
# verse5 = preprocess(raw5)
# verse6 = preprocess(raw6)
# verse7 = preprocess(raw7)
verse8 = preprocess(raw8)

# metricsAnalytics(verse1, metrics)
#
# metricsAnalytics(verse2, metrics)
#
# metricsAnalytics(verse3, metrics)
#
# metricsAnalytics(verse4, metrics)
#
# metricsAnalytics(verse5, metrics)
#
# metricsAnalytics(verse6, metrics)
#
# metricsAnalytics(verse7, metrics)

# metricsAnalytics(verse8, metrics)

build_tei_object(raw1)

print("hello")
