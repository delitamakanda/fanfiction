from django.urls import path

from categories.api import views as categories_view

urlpatterns = [
    path('category', categories_view.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>', categories_view.CategoryDetailView.as_view(), name='category-detail'),
    path('subcategory', categories_view.SubCategoryListView.as_view(), name='subcategory-list'),
    path('subcategory/<int:pk>', categories_view.SubCategoryDetailView.as_view(), name='subcategory-detail'),
]