from django.urls import path
from categories.api.views import (
	CategoryListView,
	SubCategoryDetailView,
	SubCategoryListView,
EntityCategoryListView,
)

app_name = 'categories'

urlpatterns = [
	path('', CategoryListView.as_view(), name='category-list'),
	path('subcategory/', SubCategoryListView.as_view(), name='subcategory-list'),
	path('subcategory/<slug:slug>/',
		 SubCategoryDetailView.as_view(), name='subcategory-detail'),
	path('entitycategory/', EntityCategoryListView.as_view(),
         name='entitycategory-list'),
]
