from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', views.create_article, name='create_article'),
    path('my_articles/', views.my_articles, name='my_articles'),
    path('<int:article_id>/', views.article_detail, name='article_detail'),  # Article detail view
    path('review/', views.review_articles, name='review_articles'),
    path('approve/<int:article_id>/', views.approve_article, name='approve_article'),
    path('tinymce/', include('tinymce.urls')),
    path('all_articles/', views.all_articles, name='all_articles'),
    path('<int:article_id>/', views.article_detail, name='article_detail'),  
    path('edit/<int:article_id>/', views.edit_article, name='edit_article'),  # Edit Article

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)