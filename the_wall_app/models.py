from django.db import models
import re

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['firstnameReg']) == 0:
            errors['firstnamelength'] = "First name is required."
        elif len(postData['firstnameReg']) < 3:
            errors['firstnameReg'] = "First Name must be at least 3 characters."

        if len(postData['lastnameReg']) == 0:
            errors['lastnamelength'] = "Last name is required."
        elif len(postData['lastnameReg']) < 3:
            errors['lastnameReg'] = "Last Name must be at least 3 characters."

        if len(postData['emailReg']) == 0:
            errors['emaillength'] = "Email is required."
        elif not EMAIL_REGEX.match(postData['emailReg']):    # test whether a field matches the pattern            
            errors['emailReg'] = "Invalid email address!"

        if len(postData['passwordReg']) == 0:
            errors['passwordlength'] = "Password is required."
        elif len(postData['passwordReg']) < 8:
            errors['passwordReg'] = "Password must be at least 8 characters"
            
        if postData['passwordReg'] != postData['passwordConfirm']:
            errors['passwordConfirm'] = "Passwords don't match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['loginEmail']):    # test whether a field matches the pattern            
            errors['login'] = "Invalid Email\Password"
        if len(postData['loginPassword']) < 8:
            errors['login'] = "Invalid Email\Password"
        return errors


class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    messageText = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='messages', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment_text = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='comments', on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name='comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)