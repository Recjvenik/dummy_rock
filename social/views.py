from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Discussion, DiscussionReply
from .serializers import DiscussionSerializer, DiscussionReplySerializer


class ModuleDiscussionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, module_slug):
        discussions = Discussion.objects.filter(
            module__slug=module_slug
        ).select_related('user').prefetch_related('replies')
        serializer = DiscussionSerializer(discussions, many=True)
        return Response({'discussions': serializer.data, 'count': discussions.count()})

    def post(self, request, module_slug):
        if not request.user.is_authenticated:
            return Response({'error': 'Login required'}, status=status.HTTP_401_UNAUTHORIZED)

        from modules.models import Module
        try:
            module = Module.objects.get(slug=module_slug)
        except Module.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get('title', '').strip()
        body = request.data.get('body', '').strip()
        if not title or not body:
            return Response({'error': 'Title and body required'}, status=status.HTTP_400_BAD_REQUEST)

        disc = Discussion.objects.create(module=module, user=request.user, title=title, body=body)
        return Response(DiscussionSerializer(disc).data, status=status.HTTP_201_CREATED)


class DiscussionDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            disc = Discussion.objects.get(pk=pk)
        except Discussion.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        replies = disc.replies.all()
        return Response({
            'discussion': DiscussionSerializer(disc).data,
            'replies': DiscussionReplySerializer(replies, many=True).data,
        })

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Login required'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            disc = Discussion.objects.get(pk=pk)
        except Discussion.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        body = request.data.get('body', '').strip()
        if not body:
            return Response({'error': 'Body required'}, status=status.HTTP_400_BAD_REQUEST)

        reply = DiscussionReply.objects.create(discussion=disc, user=request.user, body=body)
        return Response(DiscussionReplySerializer(reply).data, status=status.HTTP_201_CREATED)


class UpvoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        target = request.data.get('type', 'discussion')
        if target == 'reply':
            obj = DiscussionReply.objects.filter(pk=pk).first()
        else:
            obj = Discussion.objects.filter(pk=pk).first()

        if not obj:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        obj.upvotes += 1
        obj.save(update_fields=['upvotes'])
        return Response({'upvotes': obj.upvotes})


class MarkBestAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            reply = DiscussionReply.objects.select_related('discussion').get(pk=pk)
        except DiscussionReply.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        if reply.discussion.user != request.user:
            return Response({'error': 'Only the question author can mark best answer'},
                            status=status.HTTP_403_FORBIDDEN)

        # Unmark previous best
        DiscussionReply.objects.filter(discussion=reply.discussion).update(is_best_answer=False)
        reply.is_best_answer = True
        reply.save(update_fields=['is_best_answer'])
        reply.discussion.is_resolved = True
        reply.discussion.save(update_fields=['is_resolved'])
        return Response({'status': 'marked'})
