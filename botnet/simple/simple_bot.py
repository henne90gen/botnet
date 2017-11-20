from logging import getLogger

from botnet.bot_template import Bot

bot_name = 'simple_bot'
address = 'http://simple'
log = getLogger(bot_name)


def answer(question: str) -> list:
    log.info(question)
    return []


def main():
    Bot(bot_name, answer, address, 8080).start()


if __name__ == '__main__':
    main()
