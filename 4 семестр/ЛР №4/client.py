#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

host = 'localhost'
port = 9090

sock = socket.socket()
try:
    sock.connect((host, port))
    print("Соединение с сервером...")
except ConnectionRefusedError:
    print("Не удалось установить соединение с сервером. Проверьте правильность хоста и порта.")

s = input("Введите строку для отправки: ")
sock.send(s.encode())
print("Отправка данных на сервер...")
data = sock.recv(1024)
print("Приём данных от сервера...")
sock.close()
print("Разрыв соединения с сервером...")
