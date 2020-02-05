# -*- coding: utf-8 -*-
# src/models/main.py

import requests
import json
import pymongo


from operator import itemgetter 

def BD(conteudo1):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Banco"]
    customers = db["Banco"]
    customers_list = [conteudo1]
    x = customers.insert_many(customers_list)
    print(x.inserted_ids)


def get_request():
    try:
        data= requests.get("https://storage.googleapis.com/dito-questions/events.json", "Content-Type: application/json")
        if data.status_code == 200:
            return data.text
        return None
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
        return None
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else", err)
        return None


def agroup(data):
	data= data.get('events')
	groups={}
	timeline=[]
	for i in range(0, len(data)):
		event_comprou= data[i]
		if event_comprou['event'] == 'comprou':
			compra={}
			compra['timestamp']= event_comprou.get('timestamp')
			compra['revenue']= event_comprou.get('revenue')
			custom_data= event_comprou.get('custom_data')
			for i in range(0, len(custom_data)):
				if custom_data[i].get('key') == 'transaction_id':
					transaction= custom_data[i].get('value')
					compra['transaction_id']= custom_data[i].get('value')
				if custom_data[i].get('key') == 'store_name':
					compra['store_name']= custom_data[i].get('value')
			products= []
			event= False
			for j in range(0, len(data)):
				product= {}
				event_comprou_produto= data[j]
				if event_comprou_produto['event'] == 'comprou-produto':
					custom_data_produto= event_comprou_produto.get('custom_data')	
					for k in range(0, len(custom_data_produto)):
						item=custom_data_produto[k]
						if item.get('key') == 'transaction_id':
							if item.get('value') == transaction:
								event= True
					if event == True:
						for i in range(0, len(custom_data_produto)):
							if custom_data_produto[i].get('key') == 'product_name':
								product['name']= custom_data_produto[i].get('value')
							if custom_data_produto[i].get('key')  == 'product_price':
								product['price']= custom_data_produto[i].get('value')
						event= False
						products.append(product)
			compra['products']= products
			timeline.append(compra)
	timeOrder= sorted(timeline, key=itemgetter('timestamp'), reverse = True) 
	groups['timeline']= timeOrder
	BD(groups)


class CompraResult:
    def Resultado():
        if __name__ == '__main__':
            if not get_request():
                print("Not request (Exception)")
                
        return agroup(json.loads(get_request()))
