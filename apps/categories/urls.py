from django.urls import path

from apps.categories.api import views

app_name = "categories"

urlpatterns = [
    path("", views.CategoryListView.as_view(), name="category-list"),
    # Declared before "<slug:slug>/" so that it is not read as a category slug.
    path(
        "subcategory/",
        views.AllSubCategoryListView.as_view(),
        name="all-subcategory-list",
    ),
    path("<slug:slug>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path(
        "<slug:slug>/subcategories/",
        views.SubCategoryListView.as_view(),
        name="subcategory-list",
    ),
    path(
        "<slug:category_slug>/<slug:subcategory_slug>/",
        views.SubCategoryDetailView.as_view(),
        name="subcategory-detail",
    ),
    path(
        "<slug:category_slug>/<slug:subcategory_slug>/entities/",
        views.EntityCategoryListView.as_view(),
        name="entitycategory-list",
    ),
]
