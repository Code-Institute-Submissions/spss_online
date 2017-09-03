# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django import template
from accounts.forms import UserRegistrationForm, UserLoginForm
from products.models import Purchase

register = template.Library()


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(email=request.POST.get('email'),
                                   password=request.POST.get('password1'))
            if user:
                messages.success(request, "Thank you for registering")
                return redirect(reverse('profile'))
            else:
                messages.error(request, "Unable to log in. Please contact us")
    else:
        form=UserRegistrationForm()

    args={'form': form}
    args.update(csrf(request))
    return render(request, 'register.html', args)


@login_required(login_url='/login/')
def profile(request):
    purchases = Purchase.objects.filter(user_id=request.user.id).order_by('-license_end')
    today = arrow.now()
    return render(request, 'profile.html', {'purchases':purchases})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.success(request, "You have successfully logged in")
                return redirect(reverse('profile'))
            else:
                form.add_error(None, "Your email or password was not recognised")

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('index'))



