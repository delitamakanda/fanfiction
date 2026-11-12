from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from apps.categories.api.serializers import (
    CategorySerializer,
    EntityCategorySerializer,
    SubCategorySerializer,
)
from apps.categories.models import Category, EntityCategory, SubCategory
from apps.core.permissions import IsAdminOrReadOnly


class CategoryListView(generics.ListCreateAPIView):
    """Categories. Anyone can read, only staff can create."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"


class AllSubCategoryListView(generics.ListAPIView):
    """Every subcategory, with its category."""

    queryset = SubCategory.objects.select_related("category")
    serializer_class = SubCategorySerializer
    search_fields = ["name"]
    filterset_fields = ["category__slug"]


class SubCategoryListView(generics.ListAPIView):
    """Subcategories of one category."""

    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.select_related("category").filter(
            category__slug=self.kwargs.get("slug")
        )


@extend_schema_view(
    get=extend_schema(operation_id="api_v1_categories_subcategory_retrieve")
)
class SubCategoryDetailView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.select_related("category")
    serializer_class = SubCategorySerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            category__slug=self.kwargs["category_slug"],
            slug=self.kwargs["subcategory_slug"],
        )


class EntityCategoryListView(generics.ListAPIView):
    serializer_class = EntityCategorySerializer

    def get_queryset(self):
        return EntityCategory.objects.select_related("subcategory__category").filter(
            subcategory__category__slug=self.kwargs.get("category_slug"),
            subcategory__slug=self.kwargs.get("subcategory_slug"),
        )
