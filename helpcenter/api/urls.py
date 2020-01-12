from django.urls import path
from helpcenter.api import views as helpcenter_views

urlpatterns = [
    path('faq/', helpcenter_views.FoireAuxQuestionsApiView.as_view(), name='faq'),
    path('lexique/', helpcenter_views.LexiqueApiView.as_view(), name='lexique'),
]