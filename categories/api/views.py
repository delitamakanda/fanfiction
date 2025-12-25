from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from categories.api.serializers import SubCategorySerializer, CategorySerializer, EntityCategorySerializer

from categories.models import Category, SubCategory, EntityCategory

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name='category-detail'
    lookup_field = 'slug'


class SubCategoryListView(generics.ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.filter(category__slug=self.kwargs['slug'])


class SubCategoryDetailView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.select_related('category')
    serializer_class = SubCategorySerializer
    name='subcategory-detail'

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(
            queryset,
            category__slug=self.kwargs['category_slug'],
            slug=self.kwargs['subcategory_slug'],
        )


class EntityCategoryListView(generics.ListAPIView):
    serializer_class = EntityCategorySerializer
    name='entitycategory-list'

    def get_queryset(self):
        return EntityCategory.objects.filter(subcategory__category__slug=self.kwargs['category_slug'], subcategory__slug=self.kwargs['subcategory_slug'])
