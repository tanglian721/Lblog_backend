import mariadb
from flask import Flask, request, Response
import json
import loginFunction
import blogFunction
import random
from datetime import datetime
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

@app.route('/api/users', methods=['GET','POST','PATCH','DELETE'])
def user():
    if request.method == "GET":
        user = loginFunction.getUser()
        if user != None:
            return Response(json.dumps(user, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        username = request.json.get('username')
        password = request.json.get('password')
        print(username)
        if loginFunction.signUp(username, password):
            return Response("Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)    

@app.route('/api/login', methods=['POST'])
def login():
    if request.method == "POST":
        username = request.json.get('username')
        password = request.json.get('password')
        date = str(datetime.now())[0:10]
        user = loginFunction.login(username, password)
        print(user)
        if user != None:
            token = random.randint(1,10000000000)
            if loginFunction.token(token, user[2], date):
                userinfo = {
                    "username": user[0],
                    "user_id": user[2],
                    "token": token,
                }
                return Response(json.dumps(userinfo, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/api/blog', methods=['GET','POST','PATCH','DELETE'])
def blog():
    if request.method == "GET":
            print('start')
            user_id = request.args.get('user_id')
            blogs = blogFunction.getBlog(user_id)
            if user != None:
                return Response(json.dumps(blogs, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
            print('start')
            title = request.json.get('title')
            content = request.json.get('content')
            token = request.json.get('token')
            created_at = str(datetime.now())[0:19]
            newBlog = blogFunction.newBlog(title, content, created_at, token)
            if newBlog != None:
                return Response(json.dumps(newBlog, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
            print('start')
            content = request.json.get('content')
            token = request.json.get('token')
            blog_id = request.json.get('blog_id')
            newBlog = blogFunction.editBlog(content, token, blog_id)
            if newBlog != None:
                return Response(json.dumps(newBlog, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
            print("start")
            blog_id = request.json.get('blog_id')
            token = request.json.get('token')
            if blogFunction.deleteBlog(blog_id, token):
                return Response("Delete success!", mimetype="application/json", status=204)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
                
            