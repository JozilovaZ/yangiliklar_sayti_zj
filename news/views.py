from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from taggit.models import Tag
from .models import Contact,Category,Comments,News
import requests
from  django.db.models import Q
from .forms import AddNewsForm,AddCategoryForm
from django.contrib.auth import login,logout
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm




def home_page(request):
    latest_new=News.published.first()
    latest_news=News.published.exclude(id=latest_new.id)[:4]
    sport_news=News.published.filter(category__name="Sport")
    teno_news=News.published.filter(category__name="Texnologiya")
    mahaliy_news=News.published.filter(category__name="Mahalliy")
    xorij_news=News.published.filter(category__name="Xorij")

    context={
        "latest_new":latest_new,
        "latest_news":latest_news,
        "sport_news":sport_news,
        "teno_news":teno_news,
        "mahaliy_news":mahaliy_news,
        "xorij_news":xorij_news



    }
    return render(request,"index.html",context)



def seach_new_page(request):
    query=request.GET.get('q')
    response=News.published.filter(Q(title__contains=query)|Q(body__icontains=query))
    context={
        "response":response

    }
    return render(request,"searchnews.html",context)

def new_detail_page(request,slug):
    new=News.published.filter(slug=slug).first()
    # new=get_object_or_404(News,News.Status.Published,slug=slug)
    new.view_count+=1
    new.save(update_fields=['view_count'])
    comments=Comments.published.filter(new=new)
    if request.method=="POST":
        user=request.user
        if not user:
            user="Nomalum"
        comment=request.POST.get('comment')
        Comments.objects.create(
                user=user,
                new=new,
                comment=comment

        )

    context={
        "new":new,
        "comments":comments
    }
    return render(request,"single-page.html",context)



def mahalliy_page_view(request):
    mahaliy_news = News.published.filter(category__name="Mahalliy")
    context={
        "mahaliy_news":mahaliy_news

    }
    return render(request,"mahalliy.html",context)





def sport_page_view(request):
    sport_news=News.published.filter(category__name="Sport")
    context={
        "sport_news":sport_news
    }
    return render(request,"sport.html",context)



def xorij_page_view(request):
    xorijiy_news=News.published.filter(category__name="Xorij")
    context={
        "xorijiy_news":xorijiy_news
    }
    return render(request,"xorij.html",context)


def texnologiya_page_view(request):
    texnologiya_news=News.published.filter(category__name="Texnologiya")
    context={
        "texnologiya_news":texnologiya_news
    }

    return render(request,"texnologiya.html",context)





def addnew_view(request):
    if request.method=="POST":
        form=AddNewsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bosh_sahifa')
    else:
        form=AddNewsForm()
    context={
        "form":form

    }

    return render(request,"add_news.html",context)


#categoriya qo`shish
def add_category_view(request):
    if request.method=='POST':
        forms=AddCategoryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('bosh_sahifa')
    else:
            forms=AddCategoryForm()
    context={
            'forms':forms
        }
    return render(request,"categoriya_add.html",context)




def add_news_with_tags(request):
    if request.method == "POST":
        form = AddNewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save()

            # Teglarni qo'shish
            tags = request.POST.get("tags")  # Teglar bo'yicha input
            if tags:
                tag_list = tags.split(",")  # Teglarni vergul bilan ajratish
                for tag in tag_list:
                    tag_obj, created = Tag.objects.get_or_create(name=tag.strip())  # Tegni yaratish yoki olish
                    news.tags.add(tag_obj)  # Yangilikka tegni qo'shish

            return redirect('bosh_sahifa')  # Yangiliklar sahifasiga yo'naltirish
    else:
        form = AddNewsForm()

    context = {
        'form': form
    }
    return render(request, "add_newsss.html", context)



def contact_page_view(request):
    if request.method=="POST":
        full_name=request.POST.get("full_name")
        email=request.POST.get("email")
        supject=request.POST.get("supject")
        message=request.POST.get("message")

        if not full_name or not email or not supject or not message:
            context={
                "error":"Barcha maydonlarni to'ldirish majburiy"
            }
            return render(request,"contact.html",context)
        #bazaga saqlaymiz
        Contact.objects.create(
            full_name=full_name,
            email=email,
            supject=supject,
            message=message
        )

        #Telegram botga yuboramiz
        BOT_TOKEN="7606467914:AAFbSlkNaKKKP75r-rkKqnIRq2BOV2F4AsE"
        chat_id="6548938418"
        text=f"Sizga yangi Xabar bor\n"
        text+=f"Ismi {full_name}\n"
        text+=f"Email {email}\n"
        text+=f"Maqsad {supject}\n"
        text+=f"Xabar {message}\n"
        url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.post(url,data={"chat_id":chat_id,"text":text,"parse_mode":"HTML"})
        context = {
            "success": "Xabaringiz muvaffaqiyatli yuborildi"
        }
        return render(request, "contact.html", context)


    return render(request,"contact.html")








