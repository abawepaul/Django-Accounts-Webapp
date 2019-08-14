from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime
from datetime import timedelta

# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors["fname"] = "Name must have 2 or more characters! |"
        if len(postData['lname']) < 2:
            errors['lname'] =  "Name must have 2 or more characters! |"
        if len(postData['email']) < 1:
            errors['email'] =   "Name must have 1 or more characters! |"
        email_check = User.objects.filter(email = postData['email'])
        if email_check:
            errors['email'] = "Different email, please! |"
        if len(postData['password']) < 8:
            errors["password"] = "pw must have 8 or more characters! |"
        try:
            validate_email(postData['email'])
            valid_email = True
        except ValidationError:
            valid_email = False
            errors['email'] = "invalid email |"
        return errors
        



class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return (self.fname, self.lname, self.email)


