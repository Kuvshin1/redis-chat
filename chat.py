import redis
import hashlib
import time
import json

from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send, emit
app = Flask(__name__)


socketio = SocketIO(app, cors_allowed_origins='*')
r = redis.Redis(host='localhost', port=6379,db=0, decode_responses=True)

#Структура данных сообщения
class ChatMessage(object):
    def __init__(self,chatName,text,time,userName):
        if len(list(map(int,r.hkeys(chatName)))) == 0:
            self.id = 1
        else:
            self.id = max(list(map(int,r.hkeys(chatName)))) + 1
        self.chatName = chatName
        self.text = text
        self.time = time
        self.userName = userName

def tokenGen(chatName):
    return hashlib.sha256(chatName+str(time.time()))

#создаём нового пользователя, по умолчанию имеет доступ только к общей "флудилке"
def createNewUser(username, password):
    serialisedUserData = {
        'password':password,
        'tokens':[]
    }
    serialisedUserData = json.dumps(serialisedUserData)
    r.hset('users',username,serialisedUserData)
    return chats(username)


def checkForm(password,retry):
    if password == retry:
        return True
    else:
        return "passwords don't match"

#Добавляем введённый пользователем токен в базу
def addUserToChat(token,username):
    userData = json.loads(r.hget('users',username))
    userData['tokens'].append(token)
    userData = json.dumps(userData)
    r.hset('users',username,userData)
    return r.hget('chats',token)

#Добавляем сообщение в историю сообщений чата
def addMessageToDB(message):
    r.hset(message.chatName,message.id,json.dumps({
        'message':message.text,
        'time':message.time,
        'userName':message.userName
    }))

#Получаем список чатов, доступных пользователю
def getUserChatList(username):
    userData = json.loads(r.hget('users',username))
    chatNames = []
    for chat in userData['tokens']:
        name = r.hget('chats',chat)
        if name != None: 
            chatNames.append({
                'name':name,
                'token':chat
                })
    return chatNames


    # if 'token' in data.keys():
    #     data = {
    #         'name':addUserToChat(data['token'], data['username']),
    #         'token':data['token']
    #     }
    #     emit(data)
    #     #chats(data['username'])

@socketio.on('selectChat')
def handleSelectChat(data):
    print(data)
    chatName = r.hget('chats',data['token'])
    tmpdata = r.hgetall(chatName)
    data = {}
    for item in tmpdata:
        data[int(item)] = json.loads(tmpdata[item])
    print(data)
    emit('selectChat',data)

@socketio.on('addChat')
def handleAddChat(data):
    print(data)
    data = {
            'name':addUserToChat(data['token'], data['username']),
            'token':data['token']
        }
    emit('addChat',data)

@socketio.on('message')
def handleMessage(data):
    print("message:")
    print(data)
    send(data,broadcast=True)
    message = ChatMessage(data['chatName'],data['text'],time.time(),data['username']) 
    addMessageToDB(message)


@app.route('/', methods=["POST", "GET"])
def hello():
    message= ''
    username = ''
    password=''
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('pass')
        #Если пользователь новый - смотрим совпадают ли пароли, если да, то регистрируем, иначе выводим сообщение об ошибке
        if request.form.get('retry_pass'):
            validate = checkForm(password,request.form.get('retry_pass'))
            if validate == True:
                createNewUser(username,password)
            else:
                render_template('index.html',message=validate)
    
    if username != '' and password != '':
        #получаем данные о пользователе из базы
        userData = r.hget('users', username)

        if len(userData) == 0:
            message = 'Wrong login or password'
            return render_template('index.html',message=message)
        userData = json.loads(userData)
        if password == userData['password']:
            #getUserChatList()
            return chats(username)
        else:
            message='wrong login or password'
            return render_template('index.html',message=message)
    
    return render_template('index.html',message=message)

@app.route('/chats')
def chats(username):
    chatList = getUserChatList(username)
    print(chatList)
    return render_template('chatPage.html',username=username, chatList=chatList)

if __name__ == '__main__':
    socketio.run(app)