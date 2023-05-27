#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
print("Соединение с сервером...")
s = input("Введите строку для отправки: ")
sock.send(s.encode())
print("Отправка данных на сервер...")
data = sock.recv(1024)
print("Приём данных от сервера...")
sock.close()
print("Разрыв соединения с сервером...")
