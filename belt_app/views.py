from turtle import tracer
from django.shortcuts import render, redirect
from .models import User, Tree
import bcrypt
from django.contrib import messages


def login_page(request):
    return render(request, "login.html")


def add_user(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")

    password_plain = request.POST["password"]
    hash_pw = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name=request.POST["firstname"],
        last_name=request.POST["lastname"],
        email=request.POST["email"],
        password=hash_pw,
    )
    return redirect("/")  # FIXME: decide what to do when user is added


def login_user(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")

    user = User.objects.filter(email=request.POST["email"])
    if user:
        if bcrypt.checkpw(request.POST["password"].encode(), user[0].password.encode()):
            request.session["userid"] = user[0].id
            request.session["firstname"] = user[0].first_name
            request.session["lastname"] = user[0].last_name
            return redirect("/dashboard_page")  # FIXME: redirect to new page
        return redirect("/")

#input 
#
def logout(request):
    del request.session["userid"]
    del request.session["firstname"]
    del request.session["lastname"]
    return redirect("/")


def dashboard_page(request):
    if "userid" not in request.session:
        return redirect("/")
    context = {
        "trees": Tree.objects.all(),
        "trees_planted_by_user": User.objects.get(
            id=request.session["userid"],
        ).trees.all(),
    }
    return render(request, "dashboard.html", context)


def show_tree(request, tree_id):
    Tree.objects.get(id=tree_id).visitors.add(
        User.objects.get(id=request.session["userid"])
    )
    context = {
        "tree": Tree.objects.get(id=tree_id),
        "list_of_users_visited_tree": Tree.objects.get(id=tree_id).visitors.all(),
    }
    return render(request, "tree.html", context)


def show_all_trees(request):
    context = {
        # "trees": Tree.objects.all(),
        "trees_for_user": User.objects.get(id=request.session["userid"]).trees.all(),
    }
    return render(request, "all_trees.html", context)


def delete_tree(request):  # FIXME:
    my_tree = Tree.objects.get(id=request.POST["treeid"])
    my_tree.delete()
    return redirect("/user/account/")


def edit_tree(request, tree_id):
    context = {
        "tree": Tree.objects.get(id=tree_id),
    }
    return render(request, "edit_tree.html", context)


def update_tree(request, tree_id):
    errors = Tree.objects.validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/add_tree_page")

    my_tree = Tree.objects.get(id=tree_id)
    my_tree.species = request.POST["species"]
    my_tree.user = User.objects.get(id=request.session["userid"])
    my_tree.location = request.POST["location"]
    my_tree.reason = request.POST["reason"]
    my_tree.created_at = request.POST["date"]
    my_tree.save()
    return redirect("/user/account")


def add_tree_page(request):
    return render(request, "add_tree.html")


def plant_tree(request):
    errors = Tree.objects.validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/add_tree_page")

    Tree.objects.create(
        species=request.POST["species"],
        user=User.objects.get(id=request.session["userid"]),
        location=request.POST["location"],
        reason=request.POST["reason"],
        created_at=request.POST["date"],
    )
    return redirect("/dashboard_page")
