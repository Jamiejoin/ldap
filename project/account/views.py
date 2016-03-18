# coding: utf-8
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

@csrf_exempt
def login_view(request):
  username = request.POST.get('username')
  password = request.POST.get('password')
  print username
  print password
  if username and password:
    user = authenticate(username=username,password=password)
    print user
    if user is None:
      return render_to_response("login.html",{'authenticationFailed' : True})
    elif not user.is_active:
      return render_to_response("login.html",{'accountDisabled' : True})
    else:
      print '11111'
      login(request,user)
      return HttpResponseRedirect('/')
  else:
    return render_to_response("login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/account/login/')
