import json
import requests

###################################

def get_names_json_file(url : str) -> None:

    params = {
        'securities.columns': 'SECID,SHORTNAME,LOTSIZE,SECNAME,ISIN',
    }
    
    response = requests.get(url=url,params=params)
    data = response.json()

    stocks = []
    ticker_names = {}

    for item in data["securities"]['data']:
        ticker = item[0]
        company_name_short = item[1].strip()

        if len(ticker) == 5 and ticker[-1] == 'P':
            company_name_short = f"{company_name_short[:-2]}(Привилегированные)"
            company_name_short = company_name_short.replace("-","")
        elif company_name_short[len(item[1])-2:] == 'ао':
            company_name_short = company_name_short[:len(item[1])-2].strip()
            company_name_short = company_name_short.replace("-","")

        lot_size = item[2]
        company_name_full = item[3].replace('\\', '').replace('"', "'")
        isin = item[4]

        stocks.append({
            'Тикер' : ticker, 
            'Название компании' : company_name_short,
            'Размер лота' : lot_size,
            'Полное название' : company_name_full,
            'ISIN' : isin
        })
        ticker_names[ticker] = company_name_short

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(stocks,file,ensure_ascii=False, indent=2)
    with open("forpdf.json", "w", encoding="utf-8") as file:
        json.dump(ticker_names,file,ensure_ascii=False,indent=2)

def moex_price_parcer(url:str):
    params = {  
        'marketdata.columns': 'SECID,LAST'  # Тикер и последняя цена
    }

    response = requests.get(url, params=params)
    data = response.json()

    prices = {}

    for item in data["marketdata"]['data']:

        ticker = item[0]
        price = item[1]
        
        if price is None:
            price = 0

        prices[ticker] = price

    with open("stocks_price.json", "w") as file:
        json.dump(prices,file,ensure_ascii=False,indent=4) 


def main():
    url_moex = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"

    #moex_price_parcer(url=url_moex)
    get_names_json_file(url=url_moex)

if __name__ == "__main__":
    main() 