from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, HttpResponseRedirect
from .forms import ArticleForm, CommentForm
from django.contrib import messages
from .models import Article, Service
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
# def index(request):
#     return HttpResponse("Burasi index sayfasidir.")

def index(request):
    latest_articles = Article.objects.filter(is_approved=True).order_by('-created_date')[:3]
    services = Service.objects.all().order_by('-created_date')[:3]
    context = {
        'latest_articles' : latest_articles,
        'services' : services
    }
    return render(request, "index.html", context)
def about(request):
    return render(request, "about.html")


@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user).order_by("-created_date")
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)

@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale basarili bir sekilde olusturldu.")
        return redirect("index")
    context = {
        "form": form
    }
    return render(request, "addarticle.html", context)

def detail(request, id):
    # article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article, id=id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        comment.save()
        return HttpResponseRedirect(request.path_info)
    context = {
        "article": article,
        "form": form
    }
    return render(request, "detail.html", context)

@login_required(login_url="user:login")
def updateArticle(request, id):
    artcile = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=artcile)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale basarili bir sekilde guncellendi.")
        return redirect("blog:dashboard")
    context = {
        "form": form
    }
    return render(request, "update.html", context)

@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Makale basarili bir sekilde silindi.")
    return redirect("blog:dashboard")

def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword, is_approved=True)
    else:
        articles = Article.objects.filter(is_approved=True).order_by("-created_date")
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "articles": articles,
        "page_obj": page_obj,
        "keyword": keyword
    }
    return render(request, "articles.html", context)