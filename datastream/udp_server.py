import socket
from threading import Thread
from datastream.base import BaseSubtitleStreamServer


class UDPSubtitleStreamServer(BaseSubtitleStreamServer):
    def __init__(self, ip = "127.0.0.1", port = 5005):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.subscriptions = list()

    def add_subscriber(self, callback):
        self.subscriptions.append(callback)

    def __receive_messages(self):
        while True:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            for subscriptor in self.subscriptions:
                subscriptor(data.decode('utf-8'))

    def run(self):
        self.sock.bind((self.ip, self.port))
        self.thread = Thread(target=self.__receive_messages, daemon=True)
        self.thread.start()
