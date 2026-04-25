from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import requests

init(autoreset=True)

url = "https://editorial.rottentomatoes.com/guide/popular-movies/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

COL = 32  # Width of each column in characters


def get_top_30_movies():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", href=lambda h: h and "rottentomatoes.com/m/" in h)

    movies = []
    seen = set()
    for link in links:
        title = link.text.strip()
        if title and title not in seen:
            seen.add(title)
            movies.append(title)
        if len(movies) == 30:
            break

    # Fill up to 30 if less is found
    while len(movies) < 30:
        movies.append("")

    # table
    TOP = "┌" + ("─" * COL + "┬") * 2 + "─" * COL + "┐"
    MID = "├" + ("─" * COL + "┼") * 2 + "─" * COL + "┤"
    BOT = "└" + ("─" * COL + "┴") * 2 + "─" * COL + "┘"
    border = Fore.RED + Style.BRIGHT

    print(border + TOP)

    for row in range(10):
        # 3 films side by side: lines 1-10, 11-20, 21-30
        line = "│"
        for col in range(3):
            num   = row + 1 + col * 10
            title = movies[row + col * 10]

            # Shorten title if too long
            max_title = COL - 5
            if len(title) > max_title:
                title = title[:max_title - 1] + "…"

            cell = f" {num:2}. {title}"
            # .ljust fills with spaces → all cells the same width → straight lines
            cell = cell.ljust(COL)

            line += Fore.WHITE + Style.BRIGHT + cell + Fore.RED + Style.BRIGHT + "│"

        print(border + line)

        if row < 9:
            print(border + MID)

    print(border + BOT)

def show_film_info(film):
    response = requests.get(film["url"], headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # score
    score = soup.find("rt-text", {"slot": "criticsScore"})
    # beschreibung
    desc = soup.find("div", {"data-qa": "movie-info-synopsis"})

    print()
    print(Fore.YELLOW + Style.BRIGHT + f"  {film['title']}")
    print(Fore.RED    + Style.BRIGHT +  "  " + "─" * 40)

    if score:
        print(Fore.GREEN + Style.BRIGHT + f"  Tomatometer:  {score.text.strip()}%")
    if desc:
        print(Fore.WHITE + Style.DIM   + f"  {desc.text.strip()}")
    print()


def main():
    print()
    print(Fore.RED + Style.BRIGHT + r" /$$      /$$                      /$$            /$$$$$$                                  /$$   ")
    print(Fore.RED + Style.BRIGHT + r"| $$$    /$$$                     |__/           /$$__  $$                                | $$   ")
    print(Fore.RED + Style.BRIGHT + r"| $$$$  /$$$$  /$$$$$$  /$$    /$$ /$$  /$$$$$$ | $$  \__/  /$$$$$$$  /$$$$$$  /$$   /$$ /$$$$$$")
    print(Fore.RED + Style.BRIGHT + r"| $$ $$/$$ $$ /$$__  $$|  $$  /$$/| $$ /$$__  $$|  $$$$$$  /$$_____/ /$$__  $$| $$  | $$|_  $$_/")
    print(Fore.RED + Style.BRIGHT + r"| $$  $$$| $$| $$  \ $$ \  $$/$$/ | $$| $$$$$$$$ \____  $$| $$      | $$  \ $$| $$  | $$  | $$  ")
    print(Fore.RED + Style.BRIGHT + r"| $$\  $ | $$| $$  | $$  \  $$$/  | $$| $$_____/ /$$  \ $$| $$      | $$  | $$| $$  | $$  | $$ /$$")
    print(Fore.RED + Style.BRIGHT + r"| $$ \/  | $$|  $$$$$$/   \  $/   | $$|  $$$$$$$|  $$$$$$/|  $$$$$$$|  $$$$$$/|  $$$$$$/  |  $$$$/")
    print(Fore.RED + Style.BRIGHT + r"|__/     |__/ \______/     \_/    |__/ \_______/ \______/  \_______/ \______/  \______/    \___/ ")
    print()
    print(Fore.YELLOW + Style.BRIGHT + "  top 30 most popular movies right now")
    print()

    movies = get_top_30_movies()

    m = input(Fore.WHITE + Style.DIM + "drücke die nummer >> ")

    if m.isdigit() and 1 <= int(m) <= 30:
        show_film_info(movies[int(m) - 1])


if __name__ == "__main__":
    main()