from bs4 import BeautifulSoup
import requests
import time

url = "https://www.gq-magazin.de/entertainment/galerie/25-von-der-kritik-bestbewerteten-filme-netflix"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_name(headers, url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    names = soup.find_all("h2")

    result = []

    for i in names[2:]:
        span = i.find("span")
        if span:
            if "GallerySlideCaptionHedText" in str(span.get("class")):
                result.append(span.text)

    return result


def get_description(headers, url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    describtion = soup.find_all("div", class_="GallerySlideCaptionDek-dhHYMA hBLZEg")

    result = []

    for i in describtion:
        p_tags = i.find_all("p")
        if len(p_tags) > 1:
            result.append(p_tags[1].text)

    return result

def format_text(text):
    words = text.split()
    lines = []

    for i in range(0, len(words), 15):
        lines.append(" ".join(words[i:i+15]))

    return "\n".join(lines)

def combine(headers, url):
    names = get_name(headers, url)
    descriptions = get_description(headers, url)

    for i in range(len(names)):
        print(names[i])
        print(format_text(descriptions[i]))
        print("=" * 100)


def main():
    while True:
        try:
            combine(headers, url)
            break
        except Exception as e:
            print("Etwas ist schiefgelaufen,\n" , e, " \nversuche nochmal...")
            time.sleep(2.0)
            continue

main()