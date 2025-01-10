from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from .models import Article, Comment
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'articles/list.html', {'latest_articles_list': latest_articles_list})


@login_required(login_url='login')
def detail(request, article_id):
    try:
        a = Article.objects.get(id=article_id)
    except:
        raise Http404("Статья не найдена!")

    latest_comments_list = a.comment_set.order_by('-id')[:10]

    return render(request, 'articles/detail.html', {'article': a, 'latest_comments_list': latest_comments_list})


@login_required(login_url='login')
def leave_comment(request, article_id):
    try:
        a = Article.objects.get(id=article_id)
    except:
        raise Http404("Статья не найдена!")

    a.comment_set.create(
        author_name=request.POST['name'], comment_text=request.POST['text'])

    return HttpResponseRedirect(reverse('articles:detail', args=(a.id,)))


def home_view(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('articles:index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(
                request, 'Пользователь с таким именем уже существует')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('articles:index')

    return render(request, 'register.html')


@login_required
def profile(request):
    return render(request, 'profile.html')
