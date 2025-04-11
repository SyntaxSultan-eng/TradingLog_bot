import lxml
import json
import requests

from bs4 import BeautifulSoup as BS

###################################

headers = {
    "Accept" : "*/*",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0"
}

###################################

def get_names_json_file(url : str) -> None:

    stocks_data = dict()
    
    for num_page in range(1,25):
        page = requests.get(url + (f"/?page={num_page}"), headers=headers)
        html_page = BS(page.content, features="lxml")

        names_stocks = html_page.find_all("div", {"data-test" : "investment-share-results-item__name", "class" : "TextResponsive__sc-uiydf7-0 eDGUTY"})
        ticker_stocks = html_page.find_all("div", {"data-test" : "investment-share-results-item__ticker", "class" : "TextResponsive__sc-uiydf7-0 dLdrbQ"})

        for index in range(len(names_stocks)):
            if len(ticker_stocks[index].text.strip()) == 5 and ticker_stocks[index].text.strip() != "TRNFP":
                stocks_data[ticker_stocks[index].text.strip()] = (names_stocks[index].text.strip() + " привилегированные").upper()
                continue 
            stocks_data[ticker_stocks[index].text.strip()] = names_stocks[index].text.strip().upper()
        #print([i.text for i in names_stocks],[i.text for i in ticker_stocks])

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(stocks_data,file,ensure_ascii=False, indent=2)


def main():
    url_stocks_names = "https://www.banki.ru/investment/shares/russian_shares"
    get_names_json_file(url=url_stocks_names)

    # with open('data.json', 'r', encoding="utf-8") as file:
    #     data = json.load(file)
    #     print(data)
        


if __name__ == "__main__":
    main() 