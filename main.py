import requests
import csv
from bs4 import BeautifulSoup
from time import sleep

# Заголовки для передачи в метод от либы "requests"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-62b76434-418767bb1710570a46186842"}


# данная функция генерит поочерёдно ссылку на карточку с каждой игрой на странице

def get_url():
    root_url = "https://yandex.ru/games/category/new"
    response = requests.get(root_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    games_data = soup.find_all("a", class_="game-url game-card__game-info")

    for game in games_data:
        sleep(0.2)
        game_url = "https://yandex.ru" + game.get("href")
        print(game_url)
        yield game_url


# testtest = requests.get("http://yandex.ru/games/", headers=headers)
# print(testtest)

def OnlyDigits(text):
    return "".join([i for i in text if i.isdigit()])


for card_url in get_url():
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
