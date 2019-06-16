#!/usr/bin/python
# -*- coding: utf-8 -*-
from py2neo import Graph
import re
import json


graph = Graph("bolt://10.1.18.221:7687", username="neo4j", password="123456")


def parseNodeAndEdges(nodes, edges):
    nodes_list = []
    nodes_list.append(nodes)
    # 起始节点
    patten1 = re.compile("'r': \((.*?)\)-")
    # 关系1
    patten2 = re.compile("-\[:(.*?) {.*?->")
    # 中间节点
    patten3 = re.compile("->\((.*?)\)<-")
    # 关系2
    patten4 = re.compile("<-\[:(.*?) {")
    # 终止节点
    patten5 = re.compile("\}\]-\((.*?)\)")

    # 起始节点
    patten6 = re.compile("'r': \((.*?)\)<-")
    # 关系1
    patten7 = re.compile("<-\[:(.*?) {.*?-")
    # 中间节点
    patten8 = re.compile("-\((.*?)\)-")
    # 关系2
    patten9 = re.compile("\)-\[:(.*?) {\}\]->\(.*?\)\}$")
    # 终止节点
    patten10 = re.compile("\}\]->\((.*?)\)")

    list_relation = []
    for i in range(0, len(edges)):
        edge = str(edges[i])
        # print(edge)
        result1 = patten1.findall(edge)
        result2 = patten2.findall(edge)
        result3 = patten3.findall(edge)
        result4 = patten4.findall(edge)
        result5 = patten5.findall(edge)
        if (len(result1) == 0 or len(result2) == 0 or len(result3) == 0 or len(result4) == 0 or len(result5) == 0):
            result1 = patten6.findall(edge)
            result2 = patten7.findall(edge)
            result3 = patten8.findall(edge)
            result4 = patten9.findall(edge)
            result5 = patten10.findall(edge)
        dic = {}
        if (len(result1) > 0 and len(result2) > 0 and len(result3) > 0 and len(result4) > 0 and len(result5) > 0):
            dic["start_node"] = result1[0].decode('utf-8')
            dic["relation1"] = result2[0].decode('utf-8')
            dic["temp_node"] = result3[0].decode('utf-8')
            dic["relation2"] = result4[0].decode('utf-8')
            dic["end_node"] = result5[0].decode('utf-8')
            list_relation.append(dic)
    result_dic = {}
    result_dic["node"] = nodes_list
    result_dic["edges"] = list_relation
    # str_result = (str(result_dic))
    # str_result = json.dumps(result_dic, ensure_ascii=False)
    return result_dic


def get_info(cql1, cql2):
    """
    获得两个专家之间的论文,专利,项目之间的关系,这边只获取一个
    :param cql1: 查询两个节点
    :param cql2: 查询边的关系
    :return: 字典类型的节点与边
    """
    try:
        nodes = graph.run(cql1).data()[0]
    except:
        return "None"
    edges = graph.run(cql2).data()
    str_result = parseNodeAndEdges(nodes, edges)
    str_result = json.dumps(str_result, ensure_ascii=False)
    return str_result


def get_unit_connection(cql1, cql2):
    """
    获得两个专家之间关于单位的关系
    :param cql1: 节点
    :param cql2: 边
    :return: 两个专家之间的多个单位的关系
    """
    list_result = []
    dic_result = {}
    lenNodes = len(graph.run(cql1).data())
    for i in range(0, lenNodes):
        try:
            nodes = graph.run(cql1).data()[i]
        except:
            return "None"
        edges = graph.run(cql2).data()
        str_result = parseNodeAndEdges(nodes, edges)
        list_result.append(str_result)
    # dic_result["count"] = list_result
    str_result = json.dumps(list_result, ensure_ascii=False)
    return str_result


def getUnitPatentCount(cql):
    """
    根据输入的单位名称返回出对应年份的专利的数量
    :param cql:
    """
    try:
        nodes = graph.run(cql).data()[0]
    except:
        return "None"
    resultCount = json.dumps(nodes)
    resultCount = json.loads(resultCount)
    return resultCount["count(n2)"]


def getUnitPatentCount2(cql):
    """
    根据输入的单位名称返回出对应年份的专利的数量(公布时间)
    :param cql:
    """
    try:
        nodes = graph.run(cql).data()[0]
    except:
        return "None"
    resultCount = json.dumps(nodes)
    resultCount = json.loads(resultCount)
    return resultCount["count(n2)"]


def getUnitPatentNumb(cql):
    """
    查询某个地区公司的专利数，并返回排序的结果
    :param cql: MATCH (n1:Unit)-->(n2:Patent) where n1.area_level1='浙江' and n1.area_level2='杭州市'
    and n1.area_level3='江干区' RETURN n1,count(*) as numb order by numb DESC LIMIT 50
    """
    try:
        nodes = graph.run(cql).data()
    except:
        return "None"
    str_result = json.dumps(nodes, ensure_ascii=False)
    return str_result


def getUnitPatentDetail(cql1):
    """
    根据公司的名称查找其所有专利名称
    :param cql: MATCH (n1:Unit{unit:'杭州东城电子有限公司'})-[r]->(n2:Patent) RETURN n1,n2,r
    :return:
    """
    try:
        nodes = graph.run(cql1).data()
    except:
        return "None"
    # edges = graph.run(cql2).data()
    # print nodes
    # print edges
    str_result = json.dumps(nodes, ensure_ascii=False)
    return str_result


def getPatentExpert(cql):
    """
    根据专利id去查找该专利的专家
    :param cql:MATCH (n1:Patent{node_id:'62e1900e-5772-11e8-a1c8-64006a43f2fe'})-[r]->(n2:Expert) RETURN n1,n2,r
    :return:
    """
    try:
        nodes = graph.run(cql).data()
    except:
        return "None"
    str_result = json.dumps(nodes, ensure_ascii=False)
    return str_result


def getArea_code3PatentNum(cql):
    """
    获得某个某年地区(精确到区的单位数量)
    :param cql:MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市'
    and n1.area_level3='江干区' and n2.publication_date=~ '.*2016.*' RETURN count(n2)
    """
    try:
        nodes = graph.run(cql).data()[0]
    except:
        return "None"
    resultCount = json.dumps(nodes)
    resultCount = json.loads(resultCount)
    return resultCount["count(n2)"]


def getArea_code3Subject_code(cql):
    """
    获得某个区的所有专利的类别数量(9大类别+其他)
    :param cql: MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市'
    and n1.area_level3='下城区' and n2.subject_code='其他' RETURN count(n2)
    """
    try:
        nodes = graph.run(cql).data()[0]
    except:
        return "None"
    resultCount = json.dumps(nodes)
    resultCount = json.loads(resultCount)
    return resultCount["count(n2)"]


def getPatentType_Area_code3(cql):
    """
    获取一个区的所有专利的类型数量 并返回回来
    :param cql:MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市'
    and n1.area_level3='下城区' return n2.patent_type, count(n2.patent_type)
    """
    try:
        nodes = graph.run(cql).data()
    except:
        return "None"
    dic = {u"外观设计":0, u"实用新型":0, u"发明专利":0, u"其他":0}
    for node in nodes:
        # print node['n2.patent_type'], node['count(n2.patent_type)']
        typed = node['n2.patent_type']
        count = node['count(n2.patent_type)']
        dic[typed] = count
    return dic


def getSubjectPatentType_Area_code3(cql):
    """
    获取一个区域的某个领域下的所有专利
    :param cql:MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市'
    and n1.area_level3='下城区' and n2.subject_code='电子信息' RETURN n2.patent_type, count(n2.patent_type)
    """
    try:
        nodes = graph.run(cql).data()
    except:
        return "None"
    dic = {u"外观设计":0, u"实用新型":0, u"发明专利":0, u"其他":0}
    for node in nodes:
        # print node['n2.patent_type'], node['count(n2.patent_type)']
        typed = node['n2.patent_type']
        count = node['count(n2.patent_type)']
        dic[typed] = count
    return dic


def getSubjectYear_Area_code3(cql):
    """
    查询某个区 某个subject的历年专利变化情况
    :param cql: MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市' and
    n1.area_level3='下城区' and n2.subject_code='电子信息'  return n2.application_date
    """
    try:
        nodes = graph.run(cql).data()
    except:
        return "None"
    dic = {}
    # 历年专利数量初始化
    for i in range(2000, 2018):
        dic[str(i)] = 0
    i = 0
    for node in nodes:
        i += 1
        if int(str(node['n2.application_date'])[0:4]) >= 2000 and int(str(node['n2.application_date'])[0:4]) <= 2017:
            dic[str(node['n2.application_date'])[0:4]] += 1
    return dic


if __name__ == '__main__':
    # cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市' and n1.area_level3='萧山区' and n2.subject_code='电子信息'  return n2.application_date"
    # result = getSubjectYear_Area_code3(cql)
    # print result


    # cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市' and n1.area_level3='下城区' and n2.subject_code='电子信息' RETURN n2.patent_type, count(n2.patent_type)"
    # result = getSubjectPatentType_Area_code3(cql)
    # print result


    # cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市' and n1.area_level3='下城区' return n2.patent_type, count(n2.patent_type)"
    # result = getPatentType_Area_code3(cql)
    # print result



    # cql1 = "match (n1:Expert { name:'徐小良' }),(n2:Expert { name:'葛泉波' }), r = ((n1)-[*1..2]-(n2)) return n1, n2"
    # cql2 = "match (n1:Expert { name:'徐小良' }),(n2:Expert { name:'葛泉波' }), r = ((n1)-[*1..2]-(n2)) return r"
    #cql1 = "match (n1:Expert { name:'徐小良' }),(n2:Expert { name:'葛泉波' }),r = ((n1)--(:Patent)--(n2)) return n1, n2 union match (n1:Expert { name:'徐小良' }),(n2:Expert { name:'葛泉波'}),r = ((n1)--(:Project)--(n2)) return n1, n2 union match (n1:Expert { name:'徐小良' }),(n2:Expert { name:'葛泉波'}),r = ((n1)--(:Paper)--(n2)) return n1, n2"
    #cql2 = "match (n1:Expert { name:'徐小良' }),(n2:Expert { name:'葛泉波' }),r = ((n1)--(:Patent)--(n2)) return r union match (n1:Expert { name:'徐小良' }),(n2:Expert { name:'葛泉波'}),r = ((n1)--(:Project)--(n2)) return r union match (n1:Expert { name:'徐小良' }),(n2:Expert { name:'葛泉波'}),r = ((n1)--(:Paper)--(n2)) return r"
    #result = get_info(cql1, cql2)
    # cql1 = "match (n1:Expert { name:'周志华' }),(n2:Expert { name:'陈世福' }),r = ((n1)--(:Unit)--(n2)) return n1, n2"
    # cql2 = "match (n1:Expert { name:'周志华' }),(n2:Expert { name:'陈世福' }),r = ((n1)--(:Unit)--(n2)) return r"
    # result = get_unit_connection(cql1, cql2)
    # result[0] = result[0].encode('utf-8')
    # result[1] = result[1].encode('utf-8')
    # result[2] = result[2].encode('utf-8')
    # dic = {}
    # for i in range(2000, 2018):
    #     year = str(i)
    #     cql = "MATCH (n1:Unit{unit:'杭州电子科技大学'})-[r]->(n2:Patent) WHERE n2.application_date=~ '.*"+year+".*' RETURN count(n2)"
    #     result = getUnitPatentCount(cql)
    #     dic[year] = result
    # print dic

    # dic = {}
    # for i in range(2000, 2018):
    #     year = str(i)
    #     cql = "MATCH (n1:Unit{unit:'浙江大学'})-[r]->(n2:Patent) WHERE n2.publication_date=~ '.*" + year + ".*' RETURN count(n2)"
    #     result = getUnitPatentCount(cql)
    #     dic[year] = result
    # dic = json.dumps(dic, ensure_ascii=False)
    # print dic
    # print result

    # cql1 = "MATCH (n1:Unit{unit:'杭州宇聪科技有限公司'})-[r]->(n2:Patent) RETURN n1,n2"
    # # cql1 = "MATCH (n1:Unit{unit:'杭州东城电子有限公司'}),(n2:Patent),r=((n1)--(n2)) RETURN n1,n2"
    # result = getUnitPatentDetail(cql1)
    # print result

    # cql1 = "MATCH (n1:Patent{node_id:'62e1900e-5772-11e8-a1c8-64006a43f2fe'})-[r]->(n2:Expert) RETURN n1,n2"
    # # cql1 = "MATCH (n1:Unit{unit:'杭州东城电子有限公司'}),(n2:Patent),r=((n1)--(n2)) RETURN n1,n2"
    # result = getPatentExpert(cql1)
    # print result

    # dic = {}
    # for i in range(2000, 2018):
    #     year = str(i)
    #     cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市' and n1.area_level3='江干区' and n2.publication_date=~ '.*"+year+".*' RETURN count(n2)"
    #     result = getArea_code3PatentNum(cql)
    #     dic[year] = result
    # dic = json.dumps(dic, ensure_ascii=False)
    # print dic

    # """电子信息	A1
    # 生物医药	C1
    # 新材料	A4
    # 新能源与节能	A2
    # 机械电子与制造	A9
    # 资源与环境	C2
    # 化学化工	A5
    # 航空航天	A3
    # 农林牧渔	Z1
    # """
    # dic = {}
    # subject_list = ['电子信息', '生物医药', '新材料', '新能源与节能', '机械电子与制造',
    #                 '资源与环境', '化学化工', '航空航天', '农林牧渔', '其他']
    # for i in range(0, len(subject_list)):
    #     subject_code = str(subject_list[i])
    #     cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市' and " \
    #           "n1.area_level3='下城区' and n2.subject_code='"+subject_code+"' RETURN count(n2)"
    #     num = getArea_code3Subject_code(cql)
    #     dic[subject_code] = num
    # dic = json.dumps(dic, ensure_ascii=False)
    # print dic

    dic = {}
    subject_list = ['电子信息', '生物医药', '新材料', '新能源与节能', '机械电子与制造',
                    '资源与环境', '化学化工', '航空航天', '农林牧渔', '其他']
    for i in range(0, len(subject_list)):
        subject_code = str(subject_list[i])
        cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='浙江' and n1.area_level2='杭州市' and " \
              "n1.area_level3='下城区' and n2.subject_code='"+subject_code+"' and n2.patent_type='发明专利' RETURN count(n2)"
        num = getArea_code3Subject_code(cql)
        dic[subject_code] = num
    dic = json.dumps(dic, ensure_ascii=False)
    print dic
