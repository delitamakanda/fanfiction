from django.urls import path
from categories.api.views import (
	CategoryDetailView,
	CategoryListView,
	SubCategoryDetailView,
	SubCategoryListView,
)

urlpatterns = [
	path('', CategoryListView.as_view(), name='category-list'),
	path('<int:pk>/',
		 CategoryDetailView.as_view(), name='category-detail'),
	path('subcategory/', SubCategoryListView.as_view(), name='subcategory-list'),
	path('subcategory/<int:pk>/',
		 SubCategoryDetailView.as_view(), name='subcategory-detail'),
]
