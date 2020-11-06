from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Booktitle, Bookitem, CircAccount

# Functions need import
from django.contrib import messages
import datetime

# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_page(request):
    form = AuthenticationForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/viewrecord')
    return render(request, 'login.html', context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url="/login")
def view_record(request):
    username = request.user
    items = Bookitem.objects.filter(current_user=username)
    user_acc = CircAccount.objects.get(user=username)

    # numer of borrowing items
    num = len(items)

    for item in items:
        item.display_message = " "
        n = datetime.date.today() - item.duedate
        if (n.days) > 0:
            item.display_message = "Overdue {} day(s)".format(n.days)

    context = {
        'items':items,
        'user_acc':user_acc,
        'num': num,
    }
    return render(request, 'account.html', context)

@login_required(login_url="/login")
def renew_books(request):
    barcode = request.GET.get('barcode')
    item = Bookitem.objects.get(barcode=barcode)

    # get new day prepared for update
    new_duedate = datetime.date.today() + datetime.timedelta(days=14)

    # get number of day before overdue
    n = item.duedate - datetime.date.today()

    # check if renewed today
    if (item.duedate == new_duedate):
        print("two dates are equal")
        messages.warning(request, '"{}" has been renewed today'.format(item.title))
        return HttpResponseRedirect("/viewrecord")
    elif (n.days > 10):
        print("Too early")
        messages.warning(request, 'Too early to renew: "{}"'.format(item.title))
        return HttpResponseRedirect("/viewrecord")
    else:
        # add fine if
        days_of_overdue = datetime.date.today() - item.duedate
        print(days_of_overdue.days)
        if (days_of_overdue.days > 0):
            username = request.user
            user_acc = CircAccount.objects.get(user=username)
            user_acc.fine += int(days_of_overdue.days)
            user_acc.save()



        item.duedate = new_duedate
        item.renewal += 1
        item.save()
        return HttpResponseRedirect("/viewrecord")

def book_record(request, id):
    book = Booktitle.objects.get(id=id)

    # convert to subject list
    subject_column = Booktitle._meta.get_field("subjects")
    subject_data = subject_column.value_from_object(book)
    subject_list = subject_data.split("||")

    # convert to isbn list
    isbn_column = Booktitle._meta.get_field("isbn")
    isbn_data = isbn_column.value_from_object(book)
    isbn_list = isbn_data.split("||")

    # check if edition = null
    if book.edition == None:
        book.edition = ""

    # get book items
    # parameter 'title' is linked to Booktitle
    items = Bookitem.objects.filter(title=id)

    # check if checked-out


    context = {
        'book':book,
        'subjects':subject_list,
        'isbn':isbn_list,
        'items':items
    }
    return render(request, 'book_record.html', context)

def searchBySubject(request, subject):
    books = Booktitle.objects.filter(subjects__contains=subject)
    num = len(books)
    context = {
        'num': num,
        'keyword':subject,
        'books':books,
    }
    return render(request, 'search.html', context)


def searchBar(request):
    search_option = request.GET.get('search_option')
    search_words = request.GET.get('search_words')

    if (search_option=="title"):
        print("title search conducted")
        books = Booktitle.objects.filter(title__icontains=search_words)
    if (search_option=="author"):
        print("author search conducted")
        books = Booktitle.objects.filter(author__icontains=search_words)
    if (search_option=="subject"):
        print("subject search conducted")
        books = Booktitle.objects.filter(subjects__icontains=search_words)
    if (search_option=="isbn"):
        print("isbn search conducted")
        books = Booktitle.objects.filter(isbn__icontains=search_words)
#    if (search_option=="any_words"):
#        print("any_words search conducted")
#        books = Booktitle.objects.filter(series__icontains=search_words)


    num = len(books)
    context = {
        'num': num,
        'keyword':search_words,
        'books':books,
    }
    if (num == 1):
        for bk in books:
            return book_record(request, bk.id)
    return render(request, 'search.html', context)


def explain(request):
    return render(request, 'explain.html')