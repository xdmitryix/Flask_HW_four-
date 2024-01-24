# Задание
#
# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
# Каждое изображение должно сохраняться в отдельном файле, название которого соответствует
# названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого
# изображения и общем времени выполнения программы.

import time
import os
import requests
import threading
import multiprocessing
import asyncio
import aiohttp
from aiohttp import ClientSession

urls = ['https://w.forfun.com/fetch/7d/7db7d55995bd8690e98b42b2d57aa496.jpeg',
        'https://mykaleidoscope.ru/x/uploads/posts/2022-10/1666206272_76-mykaleidoscope-ru-p-kartinka-na-zastavku-oboi-79.jpg',
        'https://get.wallhere.com/photo/Paris-beautiful-france-Eiffel-Tower-city-France-1091947.jpg',
        'https://proprikol.ru/wp-content/uploads/2019/10/delfiny-krasivye-kartinki-27.jpg',
        'https://mykaleidoscope.ru/x/uploads/posts/2022-10/1666206216_27-mykaleidoscope-ru-p-kartinka-na-zastavku-oboi-27.jpg'
        ]


def download(url, filename):
    responce = requests.get(url).content
    with open(filename, "wb", ) as f:
        f.write(responce)


def synch_method():
    folder = 'data_task_four'
    start_time = time.time()
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in urls:
        name = os.path.join(folder, url.split('/')[-1])
        download(url, name)
    print(f'время синхронного метода: {time.time() - start_time}')


def thread_method():
    threads = []
    folder = 'data_task_four_thread'
    start_time = time.time()
    if not os.path.exists(folder):
        os.mkdir(folder)

    for url in urls:
        name = os.path.join(folder, url.split('/')[-1])
        t = threading.Thread(target=download, args=[url, name])
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    print(f'время многопоточного метода: {time.time() - start_time}')


def multiproc_method():
    processes = []
    folder = 'data_task_four_multiprocessor'
    start_time = time.time()
    if not os.path.exists(folder):
        os.mkdir(folder)

    for url in urls:
        name = os.path.join(folder, url.split('/')[-1])
        p = multiprocessing.Process(target=download, args=[url, name])
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    print(f'время многопроцессорного метода: {time.time() - start_time}')


async def download_asynch(url, filename):
    async with ClientSession() as session:
        async with session.get(url=url) as responce:
            context = await responce.read()
            with open(filename, "wb", ) as f:
                f.write(context)

async def method_async():
    tasks = []
    folder = 'data_task_four_asynch'
    start_time = time.time()
    if not os.path.exists(folder):
        os.mkdir(folder)

    for url in urls:
        name = os.path.join(folder, url.split('/')[-1])
        task = asyncio.ensure_future(download_asynch(url, name))
        tasks.append(task)

    await asyncio.gather(*tasks)
    print(f'время асинхронного метода: {time.time() - start_time}')




if __name__ == '__main__':
    start_time_all = time.time()
    synch_method()
    thread_method()
    multiproc_method()
    asyncio.run(method_async())
    print(f'общее время: {time.time() - start_time_all}')