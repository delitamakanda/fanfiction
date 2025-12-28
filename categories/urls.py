from django.urls import path
from categories.api.views import (
	CategoryListView,
CategoryDetailView,
	SubCategoryDetailView,
	SubCategoryListView,
EntityCategoryListView,
)

app_name = 'categories'

urlpatterns = [
	path('', CategoryListView.as_view(), name='category-list'),
	path('<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'  ),
	path('<slug:category_slug>/<slug:subcategory_slug>/', SubCategoryListView.as_view(), name='subcategory-list'),
	path('<slug:slug>/subcategories/',
		 SubCategoryDetailView.as_view(), name='subcategory-detail'),
	path('<slug:category_slug>/<slug:subcategory_slug>/entities/', EntityCategoryListView.as_view(),
         name='entitycategory-list'),
]
