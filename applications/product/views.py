from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.product.models import Product, Comment, Review, Like, Rating, Favourite
from applications.product.permissions import IsCommentOwner, IsOwner, IsReviewOwner
from applications.product.serializers import ProductSerializer, CommentSerializer, ReviewSerializer, RatingSerializer, \
    FavouriteSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['price']
    search_fields = ['title', 'description']

    @action(detail=True, methods=['POST'])
    def like(self, request, pk, *args, **kwargs):  # post/id/like/
        like_obj, _ = Like.objects.get_or_create(product_id=pk, owner=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unliked'
        return Response({'status': status})

    @action(detail=True, methods=['POST'])
    def rating(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(product_id=pk, owner=request.user)
        rating_obj.rating = request.data['rating']
        rating_obj.save()
        return Response(request.data)


class CommentAPIView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class ReviewAPIView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class FavouriteAPIView(ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    @action(detail=True, methods=['POST'])
    def favourite(self, request, pk):
        favourite_obj, _ = Favourite.objects.get_or_create(product_id=pk, owner=request.user)
        favourite_obj.is_favourite = not favourite_obj.is_favourite
        favourite_obj.save()
        status = 'favourite'
        if not favourite_obj.is_favourite:
            status = 'not favourite'
        return Response({'status': status})

    @action(detail=False, methods=['GET'])
    def get_favorite(self, request):
        products = Favourite.objects.filter(owner=request.user, is_favourite=True)
        return Response(products.data)
