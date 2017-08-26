from __future__ import unicode_literals
from django.db import models
from datetime import *
import time
import bcrypt
import re

class UsersManager(models.Manager):
    def basic_validator(self, postData):
        flag = True;
        errors = {}
        today = date.today()
        print today
        print postData


        if len(postData['name']) < 3:
            errors["name"] = "Name should be more than 3 characters"
            flag = False;
        if len(postData['username']) < 3:
            errors["username"] = "Username should be more than 3 characters"
            flag = False;
        if len(postData['password']) < 8:
            errors["password"] = "Password should be more than 8 characters"
            flag = False;
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"
            flag = False;


        if flag:
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            u = Users.objects.create(name = postData['name'], username= postData['username'], date_hired= postData['date_hired'],password= hash1)
            return(flag, u)
        else:
            return(flag, errors)

    def validate_login(self, postData):
        flag = True;
        errors = {}
        #does email exist
        try:
            user = Users.objects.get(username = postData['login_username'])
        except Exception as e:
            errors['login_username']= "User does not exist"
            return (False,errors)

        print user
        print user.password
        if bcrypt.checkpw(postData['login_password'].encode(), user.password.encode()):
            return(True, user)
        else:
            errors['login_password']= "Password incorrect"
            return (False, errors)

class ItemsManager(models.Manager):
    def items_validator(self, postData):
        flag = True;
        errors = {}
        print postData
        if len(postData['item']) < 3:
            errors["item"] = "Item must be more than 3 characters"
            flag = False;

        return(flag, errors)

class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, default='PASSWD')
    date_hired = models.DateField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UsersManager()
    def __repr__(self):
      return "<Users object: {} {}>".format(self.name, self.username)

class Items(models.Model):
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    item_uploader = models.ForeignKey(Users, related_name= "uploaded_items")
    wishlist_user= models.ManyToManyField(Users, related_name="wishlisted_items")
    objects = ItemsManager()
    def __repr__(self):
        return "<Items object: {} {}>".format(self.item, self.wishlist_user)
