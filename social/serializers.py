from rest_framework import serializers
from .models import Discussion, DiscussionReply


class DiscussionReplySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = DiscussionReply
        fields = ['id', 'body', 'upvotes', 'is_best_answer', 'created_at', 'username']

    def get_username(self, obj):
        return obj.user.email.split('@')[0]


class DiscussionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    reply_count = serializers.IntegerField(read_only=True)
    top_reply = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = ['id', 'title', 'body', 'upvotes', 'is_pinned', 'is_resolved',
                  'created_at', 'username', 'reply_count', 'top_reply']

    def get_username(self, obj):
        return obj.user.email.split('@')[0]

    def get_top_reply(self, obj):
        reply = obj.replies.filter(is_best_answer=True).first() or obj.replies.first()
        if reply:
            return DiscussionReplySerializer(reply).data
        return None
