from bs4 import BeautifulSoup
import time
from app.models import get_urls_query, zara_query
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import yagmail

def get_urls():
    while True:
        zara_urls = get_urls_query.get_zara_urls_query()
        print("The urls copied from Database")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        while True:
            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service)
                break
            
            except:
                print("The Chrome could not start. Trying again in 5 sec..")
                time.sleep(5)

        zara_stocks(zara_urls, driver, service)
        driver.close()

        time.sleep(250)

def zara_stocks(zara_urls, driver, service):
    yag = yagmail.SMTP(user='canmhmtgt@gmail.com', password='rbqh gstv vsvt jpqj')
    for url in zara_urls:
        while True:
            try:       
                driver.get(url[1])

                out_of_stocks = []
                in_and_out_of_stock_sizes = []
                try:
                    button = driver.find_element(By.CSS_SELECTOR, "button.zds-button.store-selector__button.worldwide__submit-button.zds-button--secondary")
                    
                    if button:
                        button.click()

                except:
                    pass
                
                soup = BeautifulSoup(driver.page_source, "html.parser")

                item_picture_div = soup.find("picture", class_ = "media-image")
                item_picture = item_picture_div.find_all("img", class_ = "media-image__image media__wrapper--media")
                
                for img in item_picture:
                    if img["src"] == "https://static.zara.net/stdstatic/6.40.0/images/transparent-background.png":
                        img.decompose() 

                if item_picture:
                    item_picture_url = item_picture[0]["src"]

                outher_stock_status = soup.find("span", class_ = "product-detail-show-similar-products__action-tip")
                
                if item_picture_url:
                    break


            except Exception as e:
                print("Connection problem, trying again..", e)
                time.sleep(5)



        try:
            inner_stock_status = outher_stock_status.find("span")

            if inner_stock_status and inner_stock_status.text.strip() == "TÜKENDİ":
                out_of_stocks.append(["Stok tükenmiş.", "Hiçbir beden bulunmuyor."])



        except:
            which_stock = soup.find_all("div", class_ = "size-selector-sizes-size__info")

            for stock in which_stock:

                span = stock.find("span") 
                if span and span.text.strip() == "Az sayıda ürün":
                    span.decompose()

                viewsimilars = stock.find_all("div", class_ = "size-selector-sizes-size__view-similars")

                if viewsimilars:
                    size_label = stock.find("div", class_ = "size-selector-sizes-size__label")
                    
                    if size_label:
                        sizes = size_label.text.strip()
                        in_and_out_of_stock_sizes.append(["Stok yok", sizes])

                else:
                    in_and_out_of_stock_sizes.append(["Stokta", stock.text.strip()])
                    
        
    
        if in_and_out_of_stock_sizes:
            for item in in_and_out_of_stock_sizes:
                if item is None:
                    continue
                check_zara_stock = zara_query.checking_zara_stock_same_query(url[0], item[1])

                if check_zara_stock is None:
                    zara_query.insert_zara_stock_query(item[0], item[1], url[0], item_picture_url)

                else:
                    if check_zara_stock[0] != item[0]:
                        zara_query.update_zara_stock_query(item[0], url[0], item[1])
                        print("Updated stock.")
                        subject = "Zara'ya yeni stok geldi!"
                        body = f"Merhaba. Zara'ya bu url'ye ait {url[1]}, {item[0]} beden/numara ürün gelmiştir."
                        # yag.send(to="zeynepkoparanoglu@hotmail.com", subject=subject, contents=body)

                    else:
                        print(f"The same value in Database. {item}")

            print(f"The in stock database query has been completed.")


        
        if out_of_stocks:
            for item in out_of_stocks:
                if item is None:
                    continue
                
                check_zara_stock = zara_query.checking_zara_stock_same_query(url[0], item[1])

                if check_zara_stock is None:
                    zara_query.delete_zara_stock_query(url[0])
                    zara_query.insert_zara_stock_query(item[0], item[1], url[0], item_picture_url)
                    subject = "Stok tükendi!"
                    body = f"Merhaba. Zara'da bu url'ye, {url[1]} ait stok tükenmiştir."
                    # yag.send(to="zeynepkoparanoglu@hotmail.com", subject=subject, contents=body)


                else:
                    print(f"The same value in Database. {item}")

            print(f"The out of stock database query has been completed.")


def start_app():
    get_urls()


start_app()