from logging import getLogger

import requests

from botnet.bot_template import Bot

bot_name = 'wikipedia_bot'
address = 'http://wikipedia'
log = getLogger(bot_name)


def answer(question: str) -> list:
    url = "https://en.wikipedia.org/w/api.php"
    parameters = {'action': 'query', 'format': 'json', 'list': 'search', 'srsearch': question}
    response = requests.get(url, params=parameters)
    results = []
    for elem in response.json()['query']['search']:
        results.append(elem['title'] + ": " + elem['snippet'])
    return results


def main():
    Bot(bot_name, answer, address, 8080).start()


if __name__ == '__main__':
    main()
