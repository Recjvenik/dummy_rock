from django.db import models
from django.conf import settings


class Discussion(models.Model):
    module = models.ForeignKey('modules.Module', on_delete=models.CASCADE, related_name='discussions')
    section = models.ForeignKey('modules.Section', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    upvotes = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    @property
    def reply_count(self):
        return self.replies.count()


class DiscussionReply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    upvotes = models.IntegerField(default=0)
    is_best_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_best_answer', '-upvotes', 'created_at']

    def __str__(self):
        return f"Reply to: {self.discussion.title}"
