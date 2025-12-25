from rest_framework import generics, permissions

from categories.api.serializers import SubCategorySerializer, CategorySerializer, EntityCategorySerializer

from categories.models import Category, SubCategory, EntityCategory

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='category-list'
    filter_fields = (
        'name',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
    )
    pagination_class = None


class SubCategoryListView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='subcategory-list'
    pagination_class = None


class SubCategoryDetailView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (
        permissions.AllowAny,
    )
    lookup_field = 'slug'

    name='subcategory-detail'


class EntityCategoryListView(generics.ListAPIView):
    queryset = EntityCategory.objects.all()
    serializer_class = EntityCategorySerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='entitycategory-list'
