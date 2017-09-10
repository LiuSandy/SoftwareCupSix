from flask import Flask, request, Response, jsonify, json
from flask import jsonify, make_response
from database.requestFun.statusCount import Status
from database.requestFun.predictFun import Prdt
from database.status import write_chart
from flask_cors import CORS, cross_origin
import numpy as np
import os

# print(os.getcwd())
UPLOAD_FOLDER = '\database\csv_file\\upload\\'
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
status = Status()
prdts = Prdt()


# 首页
# 走势图，各指标每天的走势情况
@app.route('/api/sum', methods=['GET', 'POST'])
def sum():
    searchWord = request.args.get('type')
    if searchWord == "cnt":
        res = status.featDay(searchWord)
    elif searchWord == "round":
        res = status.featDay(searchWord)
    elif searchWord == "inDegree":
        res = status.featDay("in_degree")
    elif searchWord == "outDegree":
        res = status.featDay("out_degree")
    else:
        res = status.featDay("page_rank")
    return json.dumps(res)


# 统计信息
@app.route('/api/degree/', methods=['GET', 'POST'])
def degree():
    data = status.getAllCount()
    searchWord = request.args.get('type')
    if searchWord == "cnt":
        saleNbr = status.saleCnt()
        saleDict = status.countSale(saleNbr)
    elif searchWord == "round":
        saleNbr = status.saleRound()
        saleDict = status.countSale(saleNbr)
    elif searchWord == "inDegree":
        saleNbr = status.indegree()
        saleDict = status.countSale(saleNbr)
    elif searchWord == "outDegree":
        saleNbr = status.outDegree()
        saleDict = status.countSale(saleNbr)
    else:
        saleNbr = status.salePageRank()
        saleDict = status.countSale(saleNbr)
    data['sale_nbr'] = saleDict
    return json.dumps(data)


# 单个详细信息
@app.route('/api/detail/', methods=['GET', 'POST'])
def detail():
    searchWord = request.args.get('type')
    reqs = status.getTrend(searchWord, [1, 91])
    return json.dumps(reqs)


# 统计详细信息
@app.route('/api/target/', methods=['GET', 'POST'])
def target():
    searchWord = request.args.get('type')
    req = status.countAllFeat(searchWord)
    return json.dumps(req)


# 查询信息
@app.route('/api/search/<saleNbr>/<dayId>', methods=['GET', 'POST'])
def search(saleNbr, dayId):
    req = status.history_info(str(saleNbr), int(dayId))
    return json.dumps(req)


# 预测信息
@app.route('/api/prdt/<saleNbr>/<dayId>', methods=['GET', 'POST'])
def prdt(saleNbr, dayId):
    targets = ['cnt', 'round', 'in_degree', 'out_degree', 'page_rank']
    result = []
    if dayId == 'all':
        for day in range(1, 31):
            dict = {}
            dict['day_id'] = day
            for target in targets:
                req = prdts.prdtData(saleNbr, target, day, 30)
                dict[target] = str(req)
            result.append(dict)
    else:
        dict = {}
        for target in targets:
            req = prdts.prdtData(saleNbr, target, int(dayId), 30)
            dict[target] = str(req)
        dict['day_id'] = dayId
        result.append(dict)
    return json.dumps(result)


@app.route('/api/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['file']
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = basedir + app.config['UPLOAD_FOLDER']
    # 保存文件
    file.save(os.path.join(file_dir, file.filename))
    return "success"


@app.route('/api/item/<fileName>', methods=['GET', 'POST'])
def itemFile(fileName):
    fileName = write_chart.main(fileName)

    return json.dumps({'boolean': True, 'fileName': fileName})


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True, threaded=True)
