# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')

class RegManager(models.Manager):
    def validate(self, postData):
        error = []
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2 or len(postData['alias']) < 2:
            error.append("All fields must have more than 2 letters.")

        if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']) or not NAME_REGEX.match(postData['alias']):
            error.append("Name fields must be letters only.")
        
        if not EMAIL_REGEX.match(postData['email']):
            error.append("Invalid Email Address.")
        
        if len(postData['password']) < 8:
            error.append("Password must be at least 8 characters.")

        if postData['password'] != postData['confirm_pass']:
            error.append("Passwords don't match!")

        hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) > 0:
            error.append("Existing user with email address")

        if len(error) > 0:
            response = {
                'status': 'error',
                'data' : error
            }
            return response
        else:
            user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], alias=postData['alias'], email=postData['email'], password=hashed_pw, birthday=postData['birthday'])
            response = {
            'status': 'good',
            'data' : user
            }
            return response

    def auth(self, postData):
        error = []
        if not EMAIL_REGEX.match(postData['email']):
            error.append("Invalid Email Address.")

        if len(postData['password']) < 8:
            error.append("Password must be at least 8 characters.")

        if postData['password'] != postData['confirm_pass']:
            error.append("Passwords don't match!")
        
        if len(error) > 0:
            response = {
                'status': 'error',
                'data' : error
            }
            return response
        else:
            retrieved_user = User.objects.filter(email=postData['email'])
            if len(retrieved_user) > 0:
                retrieved_user = retrieved_user[0]
                print retrieved_user.password
                if bcrypt.checkpw(postData['password'].encode(), retrieved_user.password.encode()):
                    print "MATCH"
                    response = {
                        'status' : 'good',
                        'data' : retrieved_user
                    }
                    return response
                else:
                    error.append("User and/or password don't match with our system.")
                    response = {
                        'status' : 'error',
                        'data': error
                    }
                    return response
            else:
                error.append("User and/or password don't match with our system.")
                response = {
                    'status' : 'error',
                    'data': error
                }
                return response
        return response



class QuoteManager(models.Manager):
    def validate(self, postData, user_id):
        error = []
        if len(postData['quoted_by']) < 4:
            error.append("Quoted by must have more than 3 characters.")

        if len(postData['message']) < 11:
            error.append("Message should have more than 10 characters")

        if len(error) > 0:
            response = {
                'status': 'error',
                'data' : error
            }
            return response
        else:
            user = User.objects.get(id=user_id)

            new_quote = Quote.objects.create(
                quoted_by = postData['quoted_by'],
                content = postData['message'],
                posted_by = user
            )

            response = {
                'status': 'good',
                'new_quote': new_quote
            }
            return response


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegManager()

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    content = models.TextField()
    posted_by = models.ForeignKey(User, related_name="quotes", null=True)
    favorited_by = models.ManyToManyField(User, related_name="fav_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()