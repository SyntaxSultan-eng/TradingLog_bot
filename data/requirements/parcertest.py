import requests
import json

url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
params = {
    'securities.columns': 'SECID,LOTSIZE',  # Кол-во акций в лоте и тикер
    'marketdata.columns': 'SECID,LAST'  # Тикер и последняя цена
}

response = requests.get(url,params=params)
data = response.json()

with open("MOEXDATA.json", "w") as file:
    json.dump(data,file,ensure_ascii=False,indent=4)

with open('data.json',"r",encoding="UTF-8") as file:
    info = json.loads(file.read())

stocks = []

for item in data["marketdata"]['data']:
    if item[0] not in info:
        continue
    ticker = item[0]
    price = item[1]
    
    if price is None:
        price = 0

    stocks.append({"ticker" : ticker, "price" : price})

index = 0
for item in data['securities']['data']:
    if item[0] not in info:
        continue
    stocks[index]['lot_size'] = item[1]
    index += 1

for key in info:
    for item in stocks:
        if key == item['ticker']:
            break
    else:
        print(key)
#ИСПРАВИТЬ DATA.JSON (в списке отсутствуют данные)
with open("stocks_price.json", "w") as file:
    json.dump(stocks,file,ensure_ascii=False,indent=4)



    
