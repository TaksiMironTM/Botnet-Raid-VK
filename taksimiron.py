#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import numpy as np
import random
import threading

app = {
    'id': '2274003',
    'key': 'hHbZxrka2uZ6jB1inYsH'
}

owner_id = 0
users = []

mode = 0

timer = False
gsec = 30
uses = 0
ls_timeout = 2
com_timeout = 2
post_timeout = 5

phrases = []

accounts = []

def getInfo(accountID, userid):
    r = requests.get('https://api.vk.com/method/users.get?access_token=' + accounts[accountID]['token'] + '&user_ids=' + str(userid) + '&v=5.103')
    return json.loads(r.text)['response'][0]

def isWhiteListed(userid):
    for user in users:
        if user == userid or owner_id == userid:
            return True
    return False

def isOwner(userid):
    if userid == owner_id:
        return True
    return False
    

def authorize(accountID):
    r = requests.get('https://oauth.vk.com/token?grant_type=password&client_id='+ app['id'] + '&client_secret=' + app['key'] + '&username=' + accounts[accountID]['login'] + '&password=' + accounts[accountID]['password'] + '&v=5.103')
    try:
        data = json.loads(r.text)
        accounts[accountID]['token'] = data['access_token']
        accounts[accountID]['user_id'] = str(data['user_id'])
        data = getInfo(accountID, accounts[accountID]['user_id'])
        print('[Авторизация | AccountID: ' + str(accountID) + '] Успешная авторизация (' + data['first_name'] + ' ' + data['last_name'] + ' | ID: ' + accounts[accountID]['user_id'] + ')')
    except Exception:
        print('[Авторизация | AccountID: ' + str(accountID) + '] Не удалось авторизоваться')

def sendFriendRequest(accountID, userid):
    r = requests.get('https://api.vk.com/method/friends.add?access_token=' + accounts[accountID]['token'] + '&user_id=' + userid + '&v=5.103')
    data = getInfo(accountID, userid)
    print('[AccountID: ' + str(accountID) + '] Отправили / приняли запрос дружбы ' + data['first_name'] + ' ' + data['last_name'])

def getLongPollServer(accountID):
    r = json.loads(requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token=' + accounts[accountID]['token'] + '&need_pts=1&lp_version=3&v=5.103').text)['response']
    return r['key'], r['server'], r['ts'], r['pts']

def getLongPollHistory(accountID):
    key, server, ts, pts = getLongPollServer(accountID)
    if accounts[accountID]['pts'] == '99999':
        accounts[accountID]['pts'] = str(pts)
    r = json.loads(requests.get('https://api.vk.com/method/messages.getLongPollHistory?access_token=' + accounts[accountID]['token'] + '&ts=' + str(ts) +'&pts=' + str(accounts[accountID]['pts']) + '&v=5.103').text)['response']
    accounts[accountID]['pts'] = str(r['new_pts'])
    return r['messages']

def sendMessage(accountID, userid, message):
    r = requests.get('https://api.vk.com/method/messages.send?access_token=' + accounts[accountID]['token'] + '&peer_id=' + str(userid) + '&message=' + message + '&random_id=' + getRandomID() + '&v=5.103')
    #print(r.text)

def sendComment(accountID, userid, post, message):
    r = requests.get('https://api.vk.com/method/wall.createComment?access_token=' + accounts[accountID]['token'] + '&owner_id=' + str(userid) + '&message=' + message + '&post_id=' + post + '&v=5.103')     
    #print(r.text)

def createPost(accountID, userid, message):
    r = requests.get('https://api.vk.com/method/wall.post?access_token=' + accounts[accountID]['token'] + '&owner_id=' + str(userid) + '&message=' + message + '&v=5.103')     
    #print(r.text)

def sendReport(accountID, userid, reason):
    r = requests.get('https://api.vk.com/method/users.report?access_token=' + accounts[accountID]['token'] + '&user_id=' + str(userid) + '&type=' + reason + '&v=5.103')     
    #print(r.text)

def addLike(accountID, userid, method, item):
    r = requests.get('https://api.vk.com/method/likes.add?access_token=' + accounts[accountID]['token'] + '&owner_id=' + str(userid) + '&item_id=' + reason + '&v=5.103&method=' + method)     
    #print(r.text)

def getComments(accountID, userid, post):
    r = requests.get('https://api.vk.com/method/wall.getComments?access_token=' + accounts[accountID]['token'] + '&owner_id=' + str(userid) + '&post_id=' + post + '&v=5.103&count=100')     
    return json.loads(r.text)['response']

def getRandomID():
    return str(np.int64(random.randint(10000, 1000000000000)))

def lsspam(target):
    global mode, timer, gsec, uses
    if mode == 1:
        sec = gsec
        timer = True
        sendMessage(0, uses, 'У вас около минуты (мб чуть больше). Учтите, что владелец может отжать атаку.')
    while mode > 0:
        if timer:
            sec = sec - 1
            if sec <= 0:
                mode = 0
                timer = False
                sendMessage(0, uses, 'Время вышло, таксист.')
                announce(uses, 'завершил работу (закончилось время)')
                break
        for i in range (0, len(accounts)):
            found = accounts[i]['phrase']
            while found == accounts[i]['phrase']:
                found = random.randint(0, len(phrases) - 1)
            accounts[i]['phrase'] = found
            sendMessage(i, target, phrases[found])
        time.sleep(2)

def comspam(target, post):
    global mode, timer, gsec, uses
    if mode == 1:
        sec = gsec
        timer = True
        sendMessage(0, uses, 'У вас около минуты (мб чуть больше). Учтите, что владелец может отжать атаку.')
    while mode > 0:
        if timer:
            sec = sec - 1
            if sec <= 0:
                mode = 0
                timer = False
                sendMessage(0, uses, 'Время вышло, таксист.')
                announce(uses, 'завершил работу (закончилось время)')
                break
        for i in range (0, len(accounts)):
            found = accounts[i]['phrase']
            while found == accounts[i]['phrase']:
                found = random.randint(0, len(phrases) - 1)
            accounts[i]['phrase'] = found
            sendComment(i, target, post, phrases[found])
        time.sleep(2)

def postspam(target):
    global mode, timer, gsec, uses
    if mode == 1:
        sec = gsec
        timer = True
        sendMessage(0, uses, 'У вас около минуты (мб чуть больше). Учтите, что владелец может отжать атаку.')
    while mode > 0:
        if timer:
            sec = sec - 1
            if sec <= 0:
                mode = 0
                timer = False
                sendMessage(0, uses, 'Время вышло, таксист.')
                announce(uses, 'завершил работу (закончилось время)')
                break
        for i in range (0, len(accounts)):
            found = accounts[i]['phrase']
            while found == accounts[i]['phrase']:
                found = random.randint(0, len(phrases) - 1)
            accounts[i]['phrase'] = found
            createPost(i, target, phrases[found])
        time.sleep(2)

def likebots(target, post):
    global mode
    for i in range(0, len(accounts)):
        if mode == 0:
            break
        comments = getComments(post)['items']
        for comment in comments:
            if mode == 0:
                break
            for k in range(0, len(accounts)):
                if comment['from_id'] == accounts[k]['user_id']:
                    addLike(i, post, 'comment', comment['id'])
                    print('liked')
                    time.sleep(2)   
                    break      

def announce(userid, what):
    data = getInfo(0, userid)
    print('[Уведомление]: Работяга ' + data['first_name'] + ' ' + data['last_name'] + ' ' + what)

def BotAI(accountID):
    global mode, target, owner_id, uses
    while True:
        time.sleep(1)
        data = getLongPollHistory(accountID)
        if len(data['items']) > 0:
            for message in data['items']:
                if str(message['from_id']) != accounts[accountID]['user_id']:
                    peerid = message['peer_id']
                    text = message['text']
                    if not isWhiteListed(message['from_id']):
                        sendMessage(accountID, peerid, '')
                        announce(message['from_id'], 'пытался воспользоваться ботом (но не админ)')
                    else:
                        if mode == 0:
                            if text.startswith('!лс'):
                                try:
                                    text = text.split()
                                    if isOwner(message['from_id']):
                                        mode = 2
                                    else:
                                        mode = 1
                                    uses = message['from_id']
                                    threading.Thread(target = lsspam, args = (text[1], )).start()
                                    sendMessage(accountID, peerid, 'Начинаем производить атаку!\nЧто бы закончить - напишите что-то.')
                                    announce(message['from_id'], 'начал флуд лички (Жертва: ' + text[1] + ')')
                                except Exception:
                                    mode = 0
                                    sendMessage(accountID, peerid, 'Используйте: !лс ID_жертвы')
                                    announce(message['from_id'], 'смотрит инструкцию по команде !лс .-.')
                            elif text.startswith('!коммент'):
                                try:
                                    text = text.split()
                                    if isOwner(message['from_id']):
                                        mode = 2
                                    else:
                                        mode = 1
                                    uses = message['from_id']
                                    threading.Thread(target = comspam, args = (text[1], text[2], )).start()
                                    sendMessage(accountID, peerid, 'Начинаем производить атаку!\nЧто бы закончить - напишите что-то.')
                                    announce(message['from_id'], 'начал флуд комментами (Жертва: ' + text[1] + ', пост: ' + text[2] + ')')
                                except Exception:
                                    mode = 0
                                    sendMessage(accountID, peerid, 'Используйте: !коммент ID_жертвы ID_поста')
                                    announce(message['from_id'], 'смотрит инструкцию по команде !коммент .-.')
                            elif text.startswith('!пост'):
                                try:
                                    text = text.split()
                                    mode = 2
                                    uses = message['from_id']
                                    threading.Thread(target = postspam, args = (text[1], )).start()
                                    sendMessage(accountID, peerid, 'Начинаем производить атаку!\nЧто бы закончить - напишите что-то.')
                                    announce(message['from_id'], 'начал флуд постами (Жертва: ' + text[1])
                                except Exception:
                                    mode = 0
                                    sendMessage(accountID, peerid, 'Используйте: !пост ID_жертвы')
                                    announce(message['from_id'], 'смотрит инструкцию по команде !пост .-.')
                            elif text.startswith('!фразы'):
                                cp = ''
                                for i in range(0, len(phrases)):
                                    cp = cp + '\n\n' + phrases[i]
                                sendMessage(accountID, peerid, 'Фразы:' + cp)
                                announce(message['from_id'], 'смотрит фразы')
                            elif text.startswith('!репорт'):
                                try:
                                    text = text.split()
                                    target = text[1]
                                    if isOwner(message['from_id']):
                                        mode = 2
                                    else:
                                        mode = 1
                                    sendMessage(accountID, peerid, 'Начинаем кидать репорты, таксярики его уработают')
                                    announce(message['from_id'], 'накидал репорты (Жертва: ' + text[1])
                                    for i in range(0, len(accounts)):
                                        sendReport(i, target, 'spam')
                                    mode = 0
                                    sendMessage(accountID, peerid, 'Закончили!')
                                except Exception:
                                    mode = 0
                                    sendMessage(accountID, peerid, 'Используйте: !репорт ID_жертвы')
                                    announce(message['from_id'], 'смотрит инструкцию по команде !репорт .-.')
                            else:
                                sendMessage(accountID, peerid, 'Приветствую, таксист! Я главный армии таксистов.\nДавайте рассмотрим имеющиеся команды:\n\n!лс ID_Жертвы - начать спам-обстрел лички\n!коммент ID_Жертвы(если группа то с минусом) ID_Поста - начать спам-обстрел поста\n!пост ID_Жертвы(если группа то с минусом) - начать спам-обстрел стены\n!фразы - посмотреть фразы\n!репорт ID_Жертвы - зарепортить челика >=)')
                                announce(message['from_id'], 'ввел хуйню или смотрит команды (' + text + ')')
                        else:
                            if isOwner(message['from_id']) or uses == message['from_id']:
                                mode = 0
                                if uses != message['from_id']:
                                    sendMessage(accountID, uses, 'Тут такое дело.. Админ отжал у тебя атаку. Ну извините, воля ТаксиМирона.')
                                    announce(uses, 'завершил работу (отжал админ)')
                                sendMessage(accountID, peerid, 'Процесс завершен')
                                announce(message['from_id'], 'завершил работу')
                            else:
                                sendMessage(accountID, peerid, 'Вы не админ, что бы завершать процесс другого таксиста!')
                                announce(message['from_id'], 'пытался заюзать бота, когда его уже юзают')

def loadJSONSettings():
    global ls_timeout, com_timeout, post_timeout, accounts, owner_id, gsec, users, phrases
    with open('./settings.json', encoding='utf-8') as f:
        data = json.load(f)
    gsec = data['time']['timer']
    ls_timeout = data['time']['ls_timeout']
    com_timeout = data['time']['com_timeout']
    post_timeout = data['time']['post_timeout']
    print('[Загрузка]: Загрузили время')
    count = -1
    for bot in data['bots']:
        count += 1
        bot = bot.split(':')
        accounts.append({
            'phrase': -1,
            'token': '',
            'user_id': '',
            'pts': '99999',
            'login': bot[0],
            'password': bot[1],
        })
    print('[Загрузка]: Загрузили ботов')
    owner_id = data['users']['owner']
    for user in data['users']['other']:
        users.append(user)
    print('[Загрузка]: Загрузили юзеров')
    for phrase in data['phrases']:
        phrases.append(phrase)
    print('[Загрузка]: Загрузили фразы')


loadJSONSettings()

for i in range(0, len(accounts)):
    authorize(i)

print('[Успех]: Бот готов к использованию! Не забудь подписаться на наши каналы:\nWhyHacks(YouTube) и @taksimironraid(TG)')
BotAI(0)
