import pymongo
from fastapi import FastAPI

app = FastAPI()

@app.get('/autocomplete')
def autocomplete():
    #client = pymongo.MongoClient("mongodb://localhost:27017/")
    #db = client["Dito"]
    #customers = db["Dito"]
    #for x in customers.find():
        #print(x)
