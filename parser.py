import requests
from bs4 import BeautifulSoup

url = "https://dungeon.su/spells/"
basic_url = "https://dungeon.su"

resp = requests.get(url)
html = resp.text
parser = BeautifulSoup(html, "html.parser")

for elements in parser.find_all("li", {'class': 'first-letter'}):
    elements.decompose()

elements = parser.select_one("ul.list-of-items.col4.double")

spells = elements.find_all("li")

urls = []
for spell in spells:
    url = spell.select_one("a")["href"]
    urls.append(basic_url + url)

for url in urls:
    resp = requests.get(url)
    html = resp.text
    parser = BeautifulSoup(html, "html.parser")

    for elements in parser.find_all("li", {'class': 'translate-by'}):
        elements.decompose()

    for elements in parser.find_all("strong"):
        elements.decompose()

    for elements in parser.find_all("h3"):
        elements.decompose()

    named = parser.select_one("h2 a.item-link").get_text()

    elements = parser.select("ul.params li")

    all_param = [element.text for element in elements]

    # print(all_param)

    print("------------------------")
    print(named)
    print("------------------------")
    level = all_param[0]
    print("Уровень: ", level)
    school = all_param[1]
    print("Школа: ", school)
    application_time = all_param[2]
    print("Время накладывания: ", application_time)
    distance = all_param[3]
    print("Дистанция: ", distance)
    components = all_param[4]
    print("Компоненты: ", components)
    duration = all_param[5]
    print("Длительность: ", duration)
    classes = all_param[6]
    print("Классы: ", classes)
    source = all_param[7]
    # print("Источник: ", source)
    description = all_param[8]
    print("Описание: ", description)
