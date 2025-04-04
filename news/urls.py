from django.urls import path
from .views import (home_page,contact_page_view ,mahalliy_page_view,sport_page_view,xorij_page_view,
                    texnologiya_page_view,seach_new_page,new_detail_page,addnew_view,add_category_view,add_news_with_tags)





urlpatterns=[
    path('',home_page, name='bosh_sahifa'),
    path("contact/", contact_page_view, name='contact_add'),
    path("catigory/", mahalliy_page_view,name='mahalliy_add'),
    path("sport/",sport_page_view, name='sport_add'),
    path("xorij/",xorij_page_view, name='xorij_add'),
    path("texnologiya/",texnologiya_page_view, name='texnologiya_add'),
    path('seach/',seach_new_page, name='qidiruv'),
    path('detail/<slug:slug>', new_detail_page, name='batafsil'),
    path("qoshish/",addnew_view,name='yangilik_qoshish'),
    path("categoriya/",add_category_view,name='kategoriy_add'),
    path('add-news/',add_news_with_tags, name='add_news_with_tags'),


]
