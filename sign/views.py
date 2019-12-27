from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
import logging

# Create your views here.
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect('/event_manage/')
            response.set_cookie('user', username, 3600)
            # response.session['user'] = username
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
    else:
        return render(request, 'index.html')



@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.COOKIES.get('user', '')
    # username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username, 'events': event_list}) 


def search_event_name(request):
    username = request.COOKIES.get('user', '')
    search_event_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains = search_event_name)
    return render(request, 'event_manage.html', {'user':username, 'events':event_list})

def search_guest_name(request):
    username = request.COOKIES.get('user', '')
    search_guest_name = request.GET.get('name', '')
    guest_list = Guest.objects.filter(realname__contains = search_guest_name)
    return render(request, 'guest_manage.html', {'user':username, 'guests':guest_list})

def guest_manage(request):
    username = request.COOKIES.get('user', '')
    guest_list = Guest.objects.all()
    return render(request, 'guest_manage.html', {'user':username, 'guests':guest_list})

def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/login_action/')
    return response

def sign_index(request, eid):
    event = get_object_or_404(Event, id = eid)
    return render(request, 'sign_index.html', {'event':event})

def sign_index_action(request, eid):
    event = get_object_or_404(Event, id = eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    logging.debug("1.")
    if not result:
        return render(request, 'sign_index.html', {'event':event, 'hint':'phone error.'})
    result = Guest.objects.filter(phone=phone, event_id = eid)
    logging.debug("2.")
    if not result:
        return render(request, 'sign_index.html', {'event':event, 'hint':'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id = eid)
    logging.debug("3.")
    if result.sign:
        return render(request, 'sign_index.html', {'event':event, 'hint':'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone, event_id = eid).update(sign='1')
        return render(request, 'sign_index.html', {'event':event, 'hint':'sign in success!', 'guest':result})