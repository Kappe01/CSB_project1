from django.shortcuts import render, redirect

from . import models
import hashlib


def index(request):
    user_id = request.session.get("user_id")
    user = models.User.objects.filter(id=user_id).first()
    print(user)
    if request.method == "GET":
        if not user:
            return redirect("/login")
        filters = request.GET.get("search")

        if not filters:
            filters = ""

        todos = models.Todo.objects.filter(
            user=user, todo__contains=filters
        ).values_list("todo")

        # connection = sqlite3.connect("db.sqlite3")
        # cursor = connection.cursor()

        # cursor.execute(
        #    f"SELECT todo FROM todo_todo WHERE user_id = ? AND todo LIKE'%?%'", (user_id, filters)
        # )

        # todos = cursor.fetchall()
        # cursor.close()
        # connection.close()
        # todos = [row[0] for row in todos]
        print(todos)
        if not todos:
            todos = ["No todos"]
        return render(request, "pages/todo.html", {"todos": todos})
    else:
        todo = request.POST.get("todo")
        if todo:
            models.Todo.objects.create(todo=todo, user=user)
        return redirect("/")


def login(request):
    if request.method == "GET":
        return render(request, "pages/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]

        print(username, password)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = models.User.objects.filter(username=username, password=hashed_password)
        if user:
            request.session["user_id"] = user[0].id
            request.session.set_expiry(1800)
            return redirect("/")
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

        if len(password) < 8:
            return redirect("/register")
        if not any(char.isdigit() for char in password):
            return redirect("/register")
        if not any(char.isupper() for char in password):
            return redirect("/register")
        if not any(char.islower() for char in password):
            return redirect("/register")
        if not any(char in "!@#$%^&*()-+" for char in password):
            return redirect("/register")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = models.User.objects.create(
            username=username,
            password=hashed_password,
            security_question=security_question,
            security_answer=security_answer,
        )
        return redirect("/login")


def forgot(request):
    # Make this a function, when called it send an email with a link to change the password

    pass


def change(request, username):
    # Make this a function, when called it open a page where the user can the change the password
    pass
