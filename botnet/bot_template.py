import logging
import os
from json import load, dump
from logging import Logger
from pprint import pformat
from typing import Callable

import schedule
import sys
from flask import Flask, request
from flask_restful import Resource, Api
from requests_futures.sessions import FuturesSession

from botnet.util import setup_logger, find_free_port, start_scheduler

session = FuturesSession()

log: Logger


# noinspection PyTypeChecker
class Bot:
    answer_func: Callable[[str], str]

    class Ping(Resource):
        """
        URL parameters:
        name (required): unique name of the calling bot
        addr (required): URI where the calling bot can be reached
        port (required): port number
        """

        def __init__(self, bot):
            self.bot = bot

        def get(self):
            name = request.args.get("name", '')
            address = request.args.get("addr", '')
            port = request.args.get("port", '')
            connection_url = address + ":" + str(port)

            log.debug("Got connection from " + name + " with address " + connection_url)

            self.bot.update_peer(name, connection_url)

            return self.bot.all_peers

    class Question(Resource):
        """
        URL parameters:
        q (required): question that is being asked
        bot: Whether a bot asked
        """

        def __init__(self, bot):
            self.bot = bot

        def get(self):
            question = request.args.get('q')
            bot_is_asking = request.args.get('bot', False)
            log.debug("Question: " + question)
            answers = []

            if not bot_is_asking:
                answers += ask_peers(self.bot.online_peers, question)

            answer = answer_func(question)
            if answer:
                answers.append(answer)

            log.debug("Answers: " + pformat(answers))
            return answers

    def __init__(self, name: str, local_answer_func: Callable[[str], list], address: str,
                 port: int = -1):
        global answer_func
        answer_func = local_answer_func
        self.name = name
        self.peers_path = os.path.join(os.path.dirname(sys.argv[0]), 'peers.json')
        self.address = address

        if port < 0:
            self.port = find_free_port()
        else:
            self.port = port

        start_scheduler()
        ping_interval = 5
        schedule.every(ping_interval).seconds.do(self.verify_peers)

        self.app = Flask(name)
        global log
        log = setup_logger(self.app, name)

        if not answer_func:
            log.error("You have to provide an answer function that takes" +
                      " in a question (string) and returns an answer (string)")
            return

        self.api = Api(self.app)
        self.api.add_resource(Bot.Ping, '/ping', resource_class_kwargs={'bot': self})
        self.api.add_resource(Bot.Question, '/question', resource_class_kwargs={'bot': self})

        @self.app.after_request
        def after_request(response):
            # this is necessary for different origin requests
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            return response

        self.all_peers = load_peers(self.peers_path)
        self.online_peers = self.all_peers.copy()

    def start(self):
        self.app.run(host='0.0.0.0', port=self.port)

    def verify_peers(self):
        # enable_debug()
        log.debug('Pinging peers')

        offline_peers, online_peers, new_peers = ping_peers(self.all_peers, self.address, self.port, self.name)

        log.info('Online: ' + pformat(online_peers))

        # removing peers that did not respond
        for name in offline_peers:
            if name in self.online_peers:
                self.online_peers.pop(name)

        # adding peers that came online since the last ping
        for name, addr in online_peers:
            self.online_peers[name] = addr

        # updating own peer list with the known peers of everyone else
        for peer_dict in new_peers:
            for name, addr in peer_dict.items():
                self.update_peer(name, addr)

    def update_peer(self, name, address):
        if name == self.name:
            return
        self.all_peers[name] = address
        save_peers(self.all_peers, self.peers_path)


def enable_debug():
    """
    This only works once the server is started.
    """
    log.setLevel(logging.DEBUG)
    for handler in log.handlers:
        if type(handler) == logging.StreamHandler:
            handler.setLevel(logging.DEBUG)


def ask_peers(peers: dict, question: str):
    answers = []
    for name, addr in peers.items():
        url = addr + '/question'
        parameters = {'q': question, 'bot': True}
        try:
            response = session.get(url, params=parameters, timeout=2).result()
            answers += response.json()
        except Exception as e:
            log.debug(str(type(e)) + ": " + str(e))

    return answers


def ping_peers(peers: dict, address: str, port: int, name: str) -> (list, list, list):
    offline_peers = []
    online_peers = []
    new_peers_list = []

    def ping_peer(peer_name, peer_address):
        log_name = peer_name + " (" + peer_address + ")"
        url = peer_address + "/ping"
        parameters = {'addr': address, 'port': port, 'name': name}
        log.debug(log_name + " ping with url " + url)
        return session.get(url, params=parameters, timeout=2), log_name, peer_name, peer_address

    futures = [ping_peer(peer_name, peer_address) for peer_name, peer_address in peers.items()]

    for future, l_name, p_name, p_address in futures:
        try:
            response = future.result()
        except Exception as e:
            log.debug(l_name + " connection error")
            log.debug(str(type(e)) + ": " + str(e))
            offline_peers.append(p_name)
        else:
            log.debug(l_name + " responded with " + pformat(response.json()))
            online_peers.append((p_name, p_address))
            new_peers_list.append(response.json())

    return offline_peers, online_peers, new_peers_list


def save_peers(peers, file_name):
    with open(file_name, 'w') as f:
        dump(peers, f)


def load_peers(file_name):
    peers = {}
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            dump(peers, f)
        return peers

    with open(file_name, 'r') as f:
        peers = load(f)
    log.info('Loaded peers ' + pformat(peers))
    return peers
