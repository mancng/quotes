# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import time

def index(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    else: 
        context = {
            'date' : time.strftime('%Y-%m-%d')
        }
    return render(request, 'myquotes/index.html', context)

def register_user(request):
    if request.method == "POST":
        potential_errors = User.objects.validate(request.POST)
        if potential_errors['status'] == "error":
            for error in potential_errors['data']:
                messages.error(request, error)
            return redirect('/')
        else:
            user_id = potential_errors['data'].id
            alias = potential_errors['data'].alias
            request.session['user_id'] = user_id
            return redirect('/quotes')
    else:
        return redirect('/')

def login_user(request):
    if request.method == "POST":
        potential_errors = User.objects.auth(request.POST)
        if potential_errors['status'] == "error":
            for error in potential_errors['data']:
                messages.error(request, error)
            return redirect('/')
        else:
            user_id = potential_errors['data'].id
            alias = potential_errors['data'].alias
            request.session['user_id'] = user_id
            print request.session['user_id']
            return redirect('/quotes')
    else:
        return redirect('/')

def logout(request):
    del request.session['user_id']
    return redirect('/')

def quotes(request):
    if 'user_id' in request.session:

        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        # all_quotes = Quote.objects.all()

        all_quotes = Quote.objects.exclude(favorited_by__id=user_id)


        user = User.objects.get(id=user_id)

        user_fav = Quote.objects.filter(favorited_by__id=user_id)


        context = {
            'quotes': all_quotes,
            'fav_quotes': user_fav,
            'user': user
        }
        return render(request, 'myquotes/quotes.html', context)
    else:
        return redirect('/')

def user(request, user_id):

    quoted_user = user_id

    user_obj = User.objects.get(id=quoted_user)

    quotes_by_user = Quote.objects.filter(posted_by=quoted_user)

    count = quotes_by_user.count()

    context = {
        'quotes_by_user': quotes_by_user,
        'count': count,
        'user_obj': user_obj
    }

    return render(request, 'myquotes/users.html', context)

def add_quote(request):
    user_id = request.session['user_id']
    if request.method=="POST":
        potential_errors = Quote.objects.validate(request.POST, user_id)
        if potential_errors['status'] == "error":
            for error in potential_errors['data']:
                messages.error(request, error)
            return redirect('/quotes')
        else:
            return redirect('/quotes')

def add_fav(request, quote_id):

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    quote_id = quote_id
    quote = Quote.objects.get(id=quote_id)

    quote.favorited_by.add(user)
    quote.save()

    return redirect('/quotes')

def remove_fav(request, quote_id):

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    quote_id = quote_id
    quote = Quote.objects.get(id=quote_id)

    to_remove = user.fav_quotes.get(id=quote_id)
    
    to_remove.delete()
    to_remove.save()

    return redirect('/quotes')