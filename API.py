# -*- coding: utf-8 -*-
from flask import Flask, Response, render_template, request
import json
from wtforms import TextField, Form
from flask import jsonify
import pymongo
from bson import json_util

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

events = [ "Comprou","Comprou Produto"]

def GetBD():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Banco"]
    customers = db["Banco"]
    #customers.delete_many({})
    compras = []
    for itens in customers.find():
        compras.append(itens)
    return compras


class SearchForm(Form):
    autocomp = TextField('Event', id='events_autocomplete')


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('autocomplete')
    return Response(json.dumps(events), mimetype='application/json')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    return render_template("index.html", form=form)

@app.route('/bd', methods=['POST'])
def bd():
    search = request.args.get('bd')
    Data = GetBD()
    del Data[0]['_id']
    response = app.response_class(
        response=json.dumps(Data[0],default=str, ensure_ascii=False).encode('latin1').decode('utf8'),
        status=200,
        content_type = 'application/json; charset=utf-8',
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)