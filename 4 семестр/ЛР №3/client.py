#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

host_prompt = "Введите имя хоста (по умолчанию: localhost): "
port_prompt = "Введите номер порта (по умолчанию: 9090): "

default_host = 'localhost'
default_port = '9090'

host = input(host_prompt) or default_host
port = input(port_prompt) or default_port
port = int(port)

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
