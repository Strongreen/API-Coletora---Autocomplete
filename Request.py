import requests
import json
import pymongo

def BD(conteudo1, conteudo2):
  client = pymongo.MongoClient("mongodb://localhost:27017/")
  db = client["Dito"]
  customers = db["Dito"]
  customers_list = [conteudo1, conteudo2]
  x = customers.insert_many(customers_list)
  #print list of the _id values of the inserted documents:
  print(x.inserted_ids)



def comprou(timestamp, revenue, transaction_id, store_name):
  Compra = {
        "timeline": 
          {
            "timestamp": timestamp,
            "revenue": revenue,
            "transaction_id": transaction_id,
            "store_name": store_name,
          }
  }
  #print(Compra)
  return Compra
  

def comprouProduto(product_price, transaction_id, product_name):
  CompraProduto = {
        "transaction_id": transaction_id,
        "products":
            [{
              "name": product_name,
              "price": product_price # somar produtos
            }]
  }
  #print(CompraProduto)
  return CompraProduto

r = requests.get("https://storage.googleapis.com/dito-questions/events.json")

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

if r.status_code == 200:

  data = json.loads(r.content)

  contador = 0
  cont = len(data['events'])

  product_price =None 
  transaction_id = None
  product_name = None 
  timestamp =None
  revenue = None
  transaction_id =None
  store_name = None
  conteudo1 = None
  conteudo2 = None


  for obj in data['events']:

    while(contador <= cont):
      
      # Comprou-Produto

      if (obj['event'] == 'comprou-produto'):
        for obj2 in obj['custom_data']:
          if (obj2['key'] == 'product_name'):
            product_name = obj2['value']
            #print("product_name: " + product_name)
          else:
            if (obj2['key']  == 'transaction_id'):
              event = obj['event']
              #print("event: " + event)
              transaction_id = obj2['value']
              #print("transaction_id: " + transaction_id)
            else:
              if (obj2['key']  == 'product_price'):
                product_price = obj2['value']
                #print("product_price: " + str(product_price))

        #comprou

      if(obj['event'] == 'comprou'):
        for obj3 in obj['custom_data']:
          if (obj3['key'] == 'transaction_id'):
            event = obj['event']
            #print("event: " + event)
            transaction_id = obj3['value']
            #print("transaction_id: " + transaction_id)
            timestamp = obj['timestamp']
            #print("timestamp: " + timestamp)
          else:
            if (obj3['key'] == 'store_name'):   
              store_name = obj3['value']
              #print("store_name: " + store_name)

              revenue = obj['revenue']
              #print("revenue: " + str(revenue))

      contador += 1

      if(obj['event'] == 'comprou-produto' and product_price != None and transaction_id != None and product_name != None):
        conteudo1 = comprouProduto(product_price, transaction_id, product_name)
        break

      if(obj['event'] == 'comprou' and revenue != None and timestamp != None and transaction_id != None and store_name != None):
        conteudo2 = comprou(timestamp, revenue, transaction_id, store_name)
        break
    contem1 = json.dumps(conteudo1)
    contem2 = json.dumps(conteudo2)
  
    BD({'timeline': {'timestamp': '2016-09-22T13:57:31.2311892-03:00', 'revenue': 250, 'transaction_id': '3029384', 'store_name': 'Patio Savassi'}}, {'transaction_id': '3029384', 'products': [{'name': 'Camisa Azul', 'price': 100}]})


else:
    print ("Failed!  Status Code : " + str(r.status_code))


