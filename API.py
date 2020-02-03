import pymongo
from fastapi import FastAPI

app = FastAPI()

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Dito"]
    customers = db["Dito"]
    for x in customers.find():
        print(x)



'''
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    value = request.args.get('term')
    sql = "select name from data_table where name like '%"+value+"%'"
    data_list = []
    cursor = customers.execute(sql)
    for row in cursor:
        data_list.append(row[0])
    customers.close()

    return jsonify(json_list=data_list)

'''