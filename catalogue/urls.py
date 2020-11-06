from django.contrib import admin
from django.urls import path
from .views import home, book_record, searchBySubject, searchBar, login_page, logout_func, view_record, renew_books, explain

urlpatterns = [
    path('', home),
    path('record/<id>/', book_record),
    path('searchBySubject/<subject>/', searchBySubject),
    path('search/', searchBar),
    path('login/', login_page),
    path('logout/', logout_func),
    path('viewrecord/', view_record),
    path('renew_books/', renew_books),
    path('explain/', explain),
]