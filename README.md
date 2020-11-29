# Botnet-Raid-VK
Привет таксист!

Прочитай обязательно инструкцию в файле Instruction!

[Видео про этот скрипт](https://vk.cc/aD0us9)

# Установка для Windows:

1. Скачать [python](https://www.python.org/), при установке нажать на галочку `add to PATH`

2. Скачать файлы с гитхаба и распаковать их в любое место

3. Заполнить файл `settings.json`

4. Перейти в папку со скриптом через терминал:
```sh
cd путь/до/папки/Botnet-Raid-VK
```

5. Прописать команды:

```sh
pip3 install requests
pip3 install numpy
```

6. Запуск: 
```sh
python taksimiron.py
```

# Установка для Termux:

1. Прописать команды:
```sh
apt update && apt upgrade
apt install python
apt install git
git clone https://github.com/TaksiMironTM/Botnet-Raid-VK
cd Botnet-Raid-VK
pip install requests
pip install numpy
```

2. После переходим в проводник и редактируем файл: settings.json (можете попробовать через nano в Termux)

3. Команды, которые нужно прописывать перед каждым запуском скрипта:
```sh
cd Botnet-Raid-VK
python taksimiron.py
```

Удачи, Таксист!
