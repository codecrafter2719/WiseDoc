from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'doctor', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'doctor__username']

    actions = ['approve_articles']

    def approve_articles(self, request, queryset):
        """
        Custom admin action to approve selected articles.
        """
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} articles approved successfully!")
    approve_articles.short_description = "Approve selected articles"
