from logging import getLogger

import requests

from botnet.bot_template import Bot

bot_name = 'steam_bot'
address = 'http://steam'
log = getLogger(bot_name)


def answer(question: str) -> str:
    log.info(question)
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/"
    try:
        games = requests.get(url).json()['applist']['apps']
    except Exception:
        return ""
    question = question.upper()
    matching_games = list(
        filter(lambda x: question in x.upper(),
               map(lambda x: x['name'], games)))
    return '\n'.join(matching_games)


def main():
    Bot(bot_name, answer, address, 8081).start()


if __name__ == '__main__':
    main()
