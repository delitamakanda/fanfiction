from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.helpcenter import views
from apps.helpcenter.api.views import (
    FlatPageApiView,
    FoireAuxQuestionsApiView,
    LexiqueApiView,
)

app_name = "helpcenter"

router = SimpleRouter()
router.register("lexique", LexiqueApiView, basename="lexique")
router.register("faq", FoireAuxQuestionsApiView, basename="faq")
router.register("pages", FlatPageApiView, basename="pages")

urlpatterns = [
    *router.urls,
    path("browse/title", views.browse_by_title, name="browse"),
    path("browse/title/<str:initial>", views.browse_by_title, name="browse_by_title"),
    path("search", views.SearchSubmitView.as_view(), name="search"),
    path(
        "search-ajax-submit",
        views.SearchAjaxSubmitView.as_view(),
        name="search-ajax-submit",
    ),
    path(
        "foire-aux-questions",
        views.foire_aux_questions_view,
        name="foire_aux_questions",
    ),
]
