
    # url(r'^main/$', views.index),
    # url(r'^create$', views.register),
    # url(r'^login$', views.login),
    # url(r'^logout$', views.logout),
    # url(r'^dashboard/$', views.dashboard),
    # url(r'^items/add$',views.add_item_get),
    # url(r'^items/newitem/$', views.add_item_post),
    # url(r'^items/(?P<id>\d+)$', views.view_item),
    # url(r'^items/delete/(?P<id>\d+)$', views.delete_item),
    # url(r'^items/wishlist/add/(?P<id>\d+)$', views.add_item_wishlist),
    # url(r'^quotes/wishlist/delete/(?P<id>\d+)$', views.delete_item_wishlist),

from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
from django.contrib import messages
import datetime
from models import *

def index(request):
    print "at home page"
    return render(request,'wish_list_app/index.html')

def register(request):
    print "I am at the register page"
    results = Users.objects.basic_validator(request.POST)
    if results[0]: #no errors
        request.session['user_id']= results[1].id
        print "I am registered"
        return redirect("/main")
    else:
        print results[1]
        for key, val in results[1].iteritems():
            print key, val
            messages.error(request, val)
        return redirect("/main")


def login(request):
    results = Users.objects.validate_login(request.POST)
    if results[0]:
        #login was successful
        request.session['user_id'] = results[1].id
        user_id = request.session['user_id']
        print "logged in"
        return redirect("dashboard/")
    else:
        #login not successful
        print "user not found"
        for key, val in results[1].iteritems():
            print key, val
            messages.error(request, val)
        return redirect("/main")

def logout(request):
    del request.session['user_id']
    return redirect ("/main")

def dashboard(request):
    if not 'user_id' in request.session:
        return redirect ("/main")

    user_wishlist_items = set(Users.objects.get(id= request.session['user_id']).wishlisted_items.all())

    print user_wishlist_items

    all_items = set(Items.objects.all())
    print all_items

    all_items.difference_update(user_wishlist_items)
    print all_items

    context = {
            "user": Users.objects.get(id=request.session['user_id']),
            "user_wishlist_items" : Users.objects.get(id=request.session['user_id']).wishlisted_items.all(),
            "items": all_items,
}
    return render(request,'wish_list_app/dashboard.html', context)

def add_item_get(request):
    print "to new item page"
    return render(request,'wish_list_app/add_item.html')

def add_item_post(request):
    if not 'user_id' in request.session:
        return redirect ("/main")
    # Item validations
    results = Items.objects.items_validator(request.POST)
    if results[0]:
        #items validation successful

        print "got new item"

        user = Users.objects.get(id = request.session['user_id'])

        print user

        item = Items.objects.create(item = request.POST['item'], item_uploader= user)

        user.wishlisted_items.add(item)

        item.wishlist_user.add(user)

        print user.wishlisted_items.all()
        print item.wishlist_user.all()

        return redirect("/dashboard/")

    else:
        #added items not successful
        print results[1]
        for key, val in results[1].iteritems():
            print key, val
            messages.error(request, val)
        return redirect("/dashboard/")

def view_item(request, id):
    if not 'user_id' in request.session:
        return redirect ("/main")
    context = {
                "item": Items.objects.get(id=id),
                "item_wishlisted_users": Items.objects.get(id=id).wishlist_user.all()
    }
    return render(request,'wish_list_app/view_item.html', context)

def add_item_wishlist(request, id):
    if not 'user_id' in request.session:
        return redirect ("/main")

    print "want to add item to wishlist"

    item = Items.objects.get(id=id)
    print item

    user = Users.objects.get(id = request.session['user_id'])
    print user

    user.wishlisted_items.add(item)
    item.wishlist_user.add(user)

    print user.wishlisted_items.all()

    return redirect("/dashboard")

def delete_item_wishlist(request,id):
    if not 'user_id' in request.session:
        return redirect ("/main")

    print "want to delete item from wishlist"

    item = Items.objects.all()

    user = Users.objects.get(id = request.session['user_id'])

    wishlisted_item = Users.objects.get(id = request.session['user_id']).wishlisted_items.get(id=id)

    user.wishlisted_items.remove(wishlisted_item)

    print user.wishlisted_items.all()

    return redirect("/dashboard")

def delete_item(request,id):
    d = Items.objects.get(id=id)
    d.delete()
    return redirect("/dashboard")
