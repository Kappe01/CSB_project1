from django.shortcuts import render, redirect

from . import models
import sqlite3


def index(request, user_id):
    user = models.User.objects.filter(id=user_id).first()
    print(user)
    if request.method == "GET":
        if not user:
            return redirect("/login")
        filters = request.GET.get("search")

        if not filters:
            filters = ""

        connection = sqlite3.connect("db.sqlite3")

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT todo FROM todo_todo WHERE user_id = {user_id} AND todo LIKE'%{filters}%'",
        )

        todos = cursor.fetchall()
        cursor.close()
        connection.close()
        todos = [row[0] for row in todos]
        print(todos)
        if not todos:
            todos = ["No todos"]
        return render(request, "pages/todo.html", {"todos": todos})
    else:
        todo = request.POST.get("todo")
        if todo:
            models.Todo.objects.create(todo=todo, user=user)
        return redirect(f"/{user.id}")


def login(request):
    if request.method == "GET":
        return render(request, "pages/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = models.User.objects.filter(username=username, password=password)
        if user:
            return redirect(f"/{user[0].id}")
        else:
            return redirect("/login")


def register(request):
    if request.method == "GET":
        return render(request, "pages/register.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        security_question = request.POST["security"]
        security_answer = request.POST["security_answer"]

        user = models.User.objects.create(
            username=username,
            password=password,
            security_question=security_question,
            security_answer=security_answer,
        )
        return redirect("/login")


def forgot(request):
    if request.method == "GET":
        return render(request, "pages/forgot.html")
    else:
        username = request.POST["username"]
        user = models.User.objects.filter(username=username)

        if user:
            return redirect(f"/change/{username}")
        else:
            return redirect("/forgot")


def change(request, username):
    if request.method == "GET":
        user = models.User.objects.filter(username=username).first()
        return render(
            request, "pages/change.html", {"security_question": user.security_question}
        )
    else:
        security_answer = request.POST["security_answer"]
        password = request.POST["password"]
        if models.User.objects.filter(
            username=username, security_answer=security_answer
        ):
            user = models.User.objects.filter(username=username).first()
            if user:
                user.password = password
                user.save()
                return redirect(f"/{user.id}")
        return redirect(f"/change/{username}")
