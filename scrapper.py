from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time
import random
import requests

#страничка яндекс-игорей
root_url = "https://yandex.ru/games/category/new"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-62b76434-418767bb1710570a46186842"}

game_url_list = []

def main():
    get_urls()
    for card_url in game_url_list:
        response = requests.get(card_url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        name_of_game = soup.find('h1', class_="game-page__title").text
        count_of_download = soup.find("span", class_="game-number__number-text").text
        # изначально count_of_download содержит неразрывные пробелы, применяем функцию OnlyDigits, перезаписывая все символы, кроме цифр
        count_of_download = OnlyDigits(count_of_download)
        rate_of_game = soup.find("span", class_="popularity-badge__rating")
        if rate_of_game is None:
            print("No rate, young game, beatch" + str(rate_of_game))
            rate_of_game = 0

        else:
            rate_of_game = rate_of_game.text
            rate_of_game = float(rate_of_game.replace(',', '.'))
        # print(name_of_game, count_of_download, rate_of_game, sep='\n', end="\n\n")

        with open('scrap_result.csv', mode='a', encoding="utf-8") as file:
            writer = csv.writer(file)
            print(name_of_game, count_of_download, rate_of_game)
            outlist = [name_of_game, count_of_download, rate_of_game]
            writer.writerow(outlist)

def OnlyDigits(text):
    return "".join([i for i in text if i.isdigit()])

# скроллим страничку и получаем ссылки на карточки всех игр
def get_urls():

    browser = webdriver.Chrome()
    browser.get(root_url)
    flag = True

    while flag:
        try:
            stop_scrolling_button = browser.find_element(By.CSS_SELECTOR, ".Button2.Button2_type_link.Button2_size_l.Button2_view_action")
        except Exception:
            randomchik = random.uniform(0.5, 2.5)
            print(randomchik)
            time.sleep(randomchik)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            flag = False
            game_cards = browser.find_elements(By.CSS_SELECTOR, ".game-url.game-card__game-info")

            for game in game_cards:
                game_url = game.get_attribute("href")
                print(game_url)
                game_url_list.append(game_url)

if __name__ == "__main__":
    main()