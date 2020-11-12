import requests
from bs4 import BeautifulSoup
import csv

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

with open("Base.csv", mode="w", encoding='utf-8') as w_file:

    names = ["Name", "Level", "School", "Application time", "Distance", "Components",
             "Duration", "Classes", "Description"]

    file_writer = csv.DictWriter(w_file, delimiter=",", fieldnames=names)
    file_writer.writeheader()

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

        level = all_param[0]
        school = all_param[1]
        app_time = all_param[2]
        distance = all_param[3]
        components = all_param[4]
        duration = all_param[5]
        classes = all_param[6]
        description = all_param[8]

        file_writer.writerow({"Name": named, "Level": level, "School": school, "Application time": app_time,
                              "Distance": distance, "Components": components, "Duration": duration,
                              "Classes": classes, "Description": description})


print("Done")

