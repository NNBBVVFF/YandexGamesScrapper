from selenium import webdriver
from selenium.webdriver.common.by import By
#import csv
import time
import random
import requests

#страничка яндекс-игорей
root_url = "https://yandex.ru/games/category/new"
game_url_list = []

def main():
    #get_urls()
    game_info("https://yandex.ru/games/?app=192879")

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


def game_info(link):
    browser2 = webdriver.Chrome()
    # browser2.implicitly_wait(10)
    browser2.maximize_window()
    browser2.get(link)
    PageSource = browser2.page_source
    print(PageSource)
    # try:
    #     rate_of_game = browser2.find_element(By.CLASS_NAME, "popularity-badge__rating").text
    # except Exception:
    #     rate_of_game = "Игра слишком свежая, оценок ещё мало"
    #     print(rate_of_game)
    # else:
    #     print(rate_of_game)
    # finally:
    #     name_of_game = browser2.find_element(By.CSS_SELECTOR, ".game-page__title").text
    #     print(name_of_game)
    #     count_of_download = OnlyDigits(browser2.find_element(By.CSS_SELECTOR, ".game-number__number-text").text)
    #     print(count_of_download)





if __name__ == "__main__":
    main()