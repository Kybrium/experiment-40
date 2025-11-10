from django.db import models
from django.conf import settings

class NewsArticle(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('draft','Draft'),('scheduled','Scheduled'),('published','Published')], default='draft')
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [models.Index(fields=['status', 'published_at'])]

    def __str__(self):
        return f"Article #{self.id} | {self.posted_at.strftime('%d.%m.%Y %H:%M:%S')}"
    
class NewsArticleTranslation(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='translations')
    language_code = models.CharField(max_length=10, choices=getattr(settings, 'LANGUAGES', None))
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'language_code'],
                name='uniq_translation_per_article_lang'
            )
        ]
        indexes = [models.Index(fields=['article', 'language_code'])]