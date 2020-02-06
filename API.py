from flask import Flask, Response, render_template, request
import json
from wtforms import TextField, Form
from flask import jsonify
import pymongo

app = Flask(__name__)

events = [ "Comprou","Comprou Produto"]

def GetBD():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Banco"]
    customers = db["Banco"]
    #customers.delete_many({})
    for x in customers.find():
        print(x)
    return x

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
    

if __name__ == '__main__':
    app.run(debug=True)
