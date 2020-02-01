from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from post_app.models import Post
from post_app.serializers import PostViewSerializer, PostCreateSerializer
from post_app.permissions import IsOwnerOrReadOnlyPost


class PostCreateView(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostViewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyPost]
