from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def registration_validator(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(data["firstname"]) < 2:
            errors["firstname"] = "firstname should be more than 2"
        if len(data["lastname"]) < 2:
            errors["lastname"] = "lastname should be more than 2"
        if not EMAIL_REGEX.match(data["email"]):
            errors["email"] = "Invalid email address"
        if len(data["email"]) < 1:
            errors["email"] = "Email can't be empty"
        if data["password"] != data["passconf"]:
            errors["password"] = "Password does not match!"
        if len(data["password"]) < 8:
            errors["password"] = "Password has to be more than 8 characters"
        return errors

    def login_validator(self, data):
        errors = {}
        if data["email"] == "":
            errors["email_empty"] = "Email can't be empty"
            return errors
        user = User.objects.filter(email=data["email"])
        if not user:
            errors["wrong_email"] = "email is not found"
            return errors
        if not bcrypt.checkpw(data["password"].encode(), user[0].password.encode()):
            errors["wrong_password"] = "Invalid password"
        return errors


class TreeManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data["species"]) < 5:
            errors["species"] = "species should be min 5 characters"
        if len(data["location"]) < 2:
            errors["location"] = "location should be min 2 characters"
        if len(data["reason"]) >= 50:
            errors["reason"] = "reason can't be more than 50 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Tree(models.Model):
    species = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="trees", on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    reason = models.TextField(null=True)
    visitors = models.ManyToManyField(User,related_name="visitors")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TreeManager()

def create_user(req):
    u