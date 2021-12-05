import requests
from bs4 import BeautifulSoup
import lxml
import json

pens_lst = []
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.52"
}

def pen_firm_func(name):
    try:
        ind = name.index('"',1)
        return name[1:ind]
    except:
        return "Фирма не указана"  
    
    
def first_page(): #получение информации с первой страницы
    url = "https://leonardo.ru/ishop/tree_3727269609/"
    req = requests.get(url = url, headers = headers)

    product_lst = BeautifulSoup(req.text,"lxml")
    product_lst = product_lst.find("div", attrs = {"class":"categories-product-list"})
    product_iter = product_lst.find_all("div", attrs = {"class":"col-lg-4 product-item"})
    #список со всеми карточками
    for el in product_iter:
        pen_name = el.find("a",attrs = {"class":"link-to-product"}).text
        firm = pen_firm_func(pen_name)
        pen_name = pen_name.replace('"','')#удаление " из за спецсимвола портиться json
        pen_price = el.find("span", attrs = {"class":"new-price"}).text
        #Имя, цены, фирма
        pens_lst.append({
            "name":f"{pen_name}",
            "price":f"{pen_price}",
            "firm":f"{firm}",
        })
    print(f"Страница 1 обработана")

def get_pen():
    url = "https://leonardo.ru/ishop/tree_3727269609/"

    req = requests.get(url = url, headers = headers)
    pagination = BeautifulSoup(req.text,"lxml").find("div", attrs={"class":"pagination"})
    pagination_lst = pagination.find_all("a") # страницы для сбора
    for i in range(2,int(pagination_lst[-2].text)+1): # # для сбора со всех страниц
        url = f"https://leonardo.ru/ishop/tree_3727269609/?pages={i}"
        req = requests.get(url = url, headers = headers)

        product_lst = BeautifulSoup(req.text,"lxml")
        product_lst = product_lst.find("div", attrs = {"class":"categories-product-list"})
        product_iter = product_lst.find_all("div", attrs = {"class":"col-lg-4 product-item"})
        #список со всеми карточками
        for el in product_iter:
            pen_name = el.find("a",attrs = {"class":"link-to-product"}).text
            firm = pen_firm_func(pen_name)
            pen_name = pen_name.replace('"','')#удаление " из за спецсимвола портиться json
            pen_price = el.find("span", attrs = {"class":"new-price"}).text
            #Имя, цены, фирма
            pens_lst.append({
                "name":f"{pen_name}",
                "price":f"{pen_price}",
                "firm":f"{firm}",
            })
        print(f"Страница {i} обработана")

        
        
        


def main():
    first_page()
    get_pen()
    with open("data.json", "w", encoding = "utf8") as f:
        json.dump(pens_lst, f, indent = 4, ensure_ascii = False)
 


if __name__ == "__main__":
    main()