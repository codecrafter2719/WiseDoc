from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.utils.html import strip_tags

@login_required
def create_article(request):
    if not hasattr(request.user, 'doctorprofile'):
        return redirect('home')  # Redirect non-doctors
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.doctor = request.user
            article.status = 'pending'  # Set status to pending
            article.save()
            return redirect('my_articles')
    else:
        form = ArticleForm()
    return render(request, 'article_writing/create_article.html', {'form': form})



def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)  # Remove `status='approved'` for debugging
    return render(request, 'article_writing/article_detail.html', {'article': article})

@login_required
def my_articles(request):
    articles = Article.objects.filter(doctor=request.user)
    return render(request, 'article_writing/my_articles.html', {'articles': articles})


@staff_member_required
def review_articles(request):
    articles = Article.objects.filter(status='pending')
    return render(request, 'article_writing/review_articles.html', {'articles': articles})

@staff_member_required
def approve_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.status = 'approved'
    article.save()
    return redirect('review_articles')


def article_detail(request, article_id):
    # Filter for approved articles only
    article = get_object_or_404(Article, id=article_id, status='approved')
    return render(request, 'article_writing/article_detail.html', {'article': article})

# def all_articles(request):
#     articles = Article.objects.filter(status='approved')
#     paginator = Paginator(articles, 10)  # Show 10 articles per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'article_writing/all_articles.html', {'page_obj': page_obj})
def all_articles(request):
    articles = Article.objects.filter(status="approved").order_by('-created_at')
    
    # Preprocess articles to strip HTML and truncate content
    for article in articles:
        article.truncated_content = truncate_content(strip_tags(article.content), 30)

    # Pagination
    paginator = Paginator(articles, 10)  # 10 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'article_writing/all_articles.html', {'page_obj': page_obj})

# Helper function to truncate content
def truncate_content(content, word_limit):
    words = content.split()
    if len(words) > word_limit:
        return " ".join(words[:word_limit]) + " ..."
    return content


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, doctor=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            article.title = title
            article.content = content
            article.status = 'pending'  # Reset status to pending for admin approval
            article.save()
            return redirect('my_articles')
    return render(request, 'article_writing/edit_article.html', {'article': article})
