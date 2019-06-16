#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import make_response
import test
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/query')
def ok():
    name1 = request.args.get('name1')
    name2 = request.args.get('name2')
    cql1 = "match (n1:Expert { name:'" +name1+ "' }),(n2:Expert { name:'" +name2+ "' }),r = ((n1)--(:Patent)--(n2)) return n1, n2 union match (n1:Expert { name:'" +name1+ "' }),(n2:Expert { name:'" +name2+ "'}),r = ((n1)--(:Project)--(n2)) return n1, n2 union match (n1:Expert { name:'" +name1+ "' }),(n2:Expert { name:'" +name2+ "'}),r = ((n1)--(:Paper)--(n2)) return n1, n2"
    cql2 = "match (n1:Expert { name:'" +name1+ "' }),(n2:Expert { name:'" +name2+ "' }),r = ((n1)--(:Patent)--(n2)) return r union match (n1:Expert { name:'" +name1+ "' }),(n2:Expert { name:'" +name2+ "'}),r = ((n1)--(:Project)--(n2)) return r union match (n1:Expert { name:'" +name1+ "' }),(n2:Expert { name:'" +name2+ "'}),r = ((n1)--(:Paper)--(n2)) return r"
    #cql1 = "match (n1:Expert { name:'" + name1 + "' }),(n2:Expert { name:'" + name2 + "' }), r = ((n1)-[*1..2]-(n2)) return n1, n2"
    #cql2 = "match (n1:Expert { name:'" + name1 + "' }),(n2:Expert { name:'" + name2 + "' }), r = ((n1)-[*1..2]-(n2)) return r"
    #print cql1
    #print cql2
    result = test.get_info(cql1, cql2)
    #print result
    # return 'hello world' + result
    rst = make_response(result)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

@app.route('/getUnit')
def unit():
    name1 = request.args.get('name1')
    name2 = request.args.get('name2')
    cql1 = "match (n1:Expert { name:'" +name1+ "' }),(n2:Expert { name:'" +name2+ "' }),r = ((n1)--(:Unit)--(n2)) return n1, n2"
    cql2 = "match (n1:Expert { name:'" +name1+ "' }),(n2:Expert { name:'" +name2+ "' }),r = ((n1)--(:Unit)--(n2)) return r"
    #cql1 = "match (n1:Expert { name:'" + name1 + "' }),(n2:Expert { name:'" + name2 + "' }), r = ((n1)-[*1..2]-(n2)) return n1, n2"
    #cql2 = "match (n1:Expert { name:'" + name1 + "' }),(n2:Expert { name:'" + name2 + "' }), r = ((n1)-[*1..2]-(n2)) return r"
    #print cql1
    #print cql2
    result = test.get_unit_connection(cql1, cql2)
    #print result
    # return 'hello world' + result
    rst = make_response(result)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

@app.route('/getUnitPatentCount')
def getPatent():
    unitName = request.args.get('unitName')
    dic = {}
    for i in range(2000, 2018):
        year = str(i)
        cql = "MATCH (n1:Unit{unit:'"+unitName+"'})-[r]->(n2:Patent) WHERE n2.application_date=~ '.*" + year + ".*' RETURN count(n2)"
        result = test.getUnitPatentCount(cql)
        dic[year] = result
    #print result
    # return 'hello world' + result
    dic = json.dumps(dic, ensure_ascii=False)
    dic = str(dic)
    rst = make_response(dic)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

@app.route('/getUnitPatentCount2')
def getPatent2():
    unitName = request.args.get('unitName')
    dic = {}
    for i in range(2000, 2018):
        year = str(i)
        cql = "MATCH (n1:Unit{unit:'"+unitName+"'})-[r]->(n2:Patent) WHERE n2.publication_date=~ '.*" + year + ".*' RETURN count(n2)"
        result = test.getUnitPatentCount(cql)
        dic[year] = result
    #print result
    # return 'hello world' + result
    dic = str(dic)
    rst = make_response(dic)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getUnitPatentNum/area_level3')
def getUnitPatentNum_level3():
    level1 = request.args.get('level1')
    level2 = request.args.get('level2')
    level3 = request.args.get('level3')
    limitNum = request.args.get('limitNum')
    cql1 = "MATCH (n1:Unit)-->(n2:Patent) where n1.area_level1='"+level1+"' and n1.area_level2='"+level2+"' and n1.area_level3='"+level3+"' RETURN n1,count(*) as numb order by numb DESC LIMIT "+limitNum+""
    result = test.getUnitPatentNumb(cql1)
    #print result
    # return 'hello world' + result
    rst = make_response(result)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getUnitPatentDetail')
def getUnitPatent():
    unitName = request.args.get('unitName')
    limitNum = request.args.get('limitNum')
    cql1 = "MATCH (n1:Unit{unit:'"+unitName+"'})-[r]->(n2:Patent) RETURN n1,n2"
    result = test.getUnitPatentNumb(cql1)
    #print result
    # return 'hello world' + result
    rst = make_response(result)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getPatentExpert')
def PatentExpert():
    Patent_id = request.args.get('Patent_id')
    cql1 = "MATCH (n1:Patent{node_id:'"+Patent_id+"'})-[r]->(n2:Expert) RETURN n1,n2"
    result = test.getPatentExpert(cql1)
    #print result
    # return 'hello world' + result
    rst = make_response(result)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getUnitPatentPerYearNum/area_level3')
def getareaPatentNum():
    level1 = request.args.get('level1')
    level2 = request.args.get('level2')
    level3 = request.args.get('level3')
    dic = {}
    for i in range(2000, 2018):
        year = str(i)
        if level2 != "":
            cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level2='"+level2+"' " \
                  "and n1.area_level3='"+level3+"' and n2.publication_date=~ '.*"+year+".*' RETURN count(n2)"
        else:
            cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='" + level1 + "'and n1.area_level3='" + level3 + "' and n2.publication_date=~ '.*" + year + ".*' RETURN count(n2)"
        result = test.getArea_code3PatentNum(cql)
        dic[year] = result
    #print result
    # return 'hello world' + result
    dic = json.dumps(dic, ensure_ascii=False)
    dic = str(dic)
    rst = make_response(dic)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getUnitPatentSubject_code/area_level3')
def getareaPatentSubject_code():
    level1 = request.args.get('level1')
    level2 = request.args.get('level2')
    level3 = request.args.get('level3')
    subject_list = ['电子信息', '生物医药', '新材料', '新能源与节能', '机械电子与制造',
                    '资源与环境', '化学化工', '航空航天', '农林牧渔', '其他']
    dic = {}
    for i in range(0, len(subject_list)):
        subject_code = str(subject_list[i]).decode('utf-8')
        if level2 != "":
            cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level2='"+level2+"' and " \
              "n1.area_level3='"+level3+"' and n2.subject_code='"+subject_code+"' RETURN count(n2)"
        else:
            cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level3='"+level3+"' and n2.subject_code='"+subject_code+"' RETURN count(n2)"
        result = test.getArea_code3Subject_code(cql)
        dic[subject_code] = result
    #print result
    # return 'hello world' + result
    dic = json.dumps(dic, ensure_ascii=False)
    rst = make_response(dic)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getUnitPatentSubject_code/area_level3/PatentType1')
def getareaPatentSubject_codePatentType1():
    level1 = request.args.get('level1')
    level2 = request.args.get('level2')
    level3 = request.args.get('level3')
    subject_list = ['电子信息', '生物医药', '新材料', '新能源与节能', '机械电子与制造',
                    '资源与环境', '化学化工', '航空航天', '农林牧渔', '其他']
    type = request.args.get('type')
    dic = {}
    for i in range(0, len(subject_list)):
        subject_code = str(subject_list[i]).decode('utf-8')
        if level2 != "":
            cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level2='"+level2+"' and " \
              "n1.area_level3='"+level3+"' and n2.subject_code='"+subject_code+"' and n2.patent_type='"+type+"' RETURN count(n2)"
        else:
            cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level3='"+level3+"' and n2.subject_code='"+subject_code+"' and n2.patent_type='"+type+"' RETURN count(n2)"
        result = test.getArea_code3Subject_code(cql)
        dic[subject_code] = result
    #print result
    # return 'hello world' + result
    dic = json.dumps(dic, ensure_ascii=False)
    rst = make_response(dic)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getUnitPatentSubject_code/area_level3/PatentType2')
def getareaPatentSubject_codePatentType2():
    level1 = request.args.get('level1')
    level2 = request.args.get('level2')
    level3 = request.args.get('level3')
    subject_list = ['电子信息', '生物医药', '新材料', '新能源与节能', '机械电子与制造',
                    '资源与环境', '化学化工', '航空航天', '农林牧渔', '其他']
    type1 = request.args.get('type1')
    type2 = request.args.get('type2')

    dic = {}
    for i in range(0, len(subject_list)):
        subject_code = str(subject_list[i]).decode('utf-8')
        if level2 != "":
            cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level2='"+level2+"' and " \
              "n1.area_level3='"+level3+"' and n2.subject_code='"+subject_code+"' and (n2.patent_type='"+type1+"' or n2.patent_type='"+type2+"') RETURN count(n2)"
        else:
            cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level3='"+level3+"' and n2.subject_code='"+subject_code+"' and (n2.patent_type='"+type1+"' or n2.patent_type='"+type2+"') RETURN count(n2)"
        result = test.getArea_code3Subject_code(cql)
        dic[subject_code] = result
    #print result
    # return 'hello world' + result
    dic = json.dumps(dic, ensure_ascii=False)
    rst = make_response(dic)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getPatentType_area_level3')
def getPatentBytype():
    level1 = request.args.get('level1')
    level2 = request.args.get('level2')
    level3 = request.args.get('level3')

    if level2 != "":
        cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and " \
              "n1.area_level2='"+level2+"' and n1.area_level3='"+level3+"' return n2.patent_type, count(n2.patent_type)"
    else:
        cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level3='"+level3+"' return n2.patent_type, count(n2.patent_type)"
    result = test.getPatentType_Area_code3(cql)
    #print result
    # return 'hello world' + result
    dic = json.dumps(result, ensure_ascii=False)
    rst = make_response(dic)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getSubjectPatentType_area_level3')
def getSubjectPatentBytype():
    level1 = request.args.get('level1')
    level2 = request.args.get('level2')
    level3 = request.args.get('level3')
    subject = request.args.get('subject')
    if level2 != "":
        cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level2='"+level2+"' and n1.area_level3='"+level3+"' and n2.subject_code='"+subject+"' RETURN n2.patent_type, count(n2.patent_type)"
    else:
        cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level3='"+level3+"' and n2.subject_code='"+subject+"' RETURN n2.patent_type, count(n2.patent_type)"
    result = test.getPatentType_Area_code3(cql)
    #print result
    # return 'hello world' + result
    dic = json.dumps(result, ensure_ascii=False)
    rst = make_response(dic)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/getSubjectYear_area_level3')
def getSubjectYear():
    level1 = request.args.get('level1')
    level2 = request.args.get('level2')
    level3 = request.args.get('level3')
    subject = request.args.get('subject')
    if level2 != "":
        cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level2='"+level2+"' and n1.area_level3='"+level3+"' and n2.subject_code='"+subject+"'  return n2.application_date"
    else:
        cql = "MATCH (n1:Unit)-->(n2:Patent) WHERE n1.area_level1='"+level1+"' and n1.area_level3='"+level3+"' and n2.subject_code='"+subject+"'  return n2.application_date"
    result = test.getSubjectYear_Area_code3(cql)
    #print result
    # return 'hello world' + result
    dic = json.dumps(result, ensure_ascii=False)
    rst = make_response(dic)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
