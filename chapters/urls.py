from django.urls import path
from chapters.api.views import (
     ChapterListApiView,
     ChapterCreateApiView,
     ChapterDetailView,
generate_chapter_summary,
list_styles_prompts,
autosave_chapter
)

app_name = 'chapters'

urlpatterns = [
path('<int:fanfic>/list/',
         ChapterListApiView.as_view(), name='chapter-list-by-fanfic'),
    path('create/', ChapterCreateApiView.as_view(), name='chapter-create'),
    path('<int:pk>/',
         ChapterDetailView.as_view(), name='chapter-detail'),
	path('generate', generate_chapter_summary, name='generate'),
	path('styles-prompts', list_styles_prompts, name='styles-prompts'),
	# fanfic_id is passed as a parameter to the view
	path('<int:fanfic_id>/autosave', autosave_chapter, name='autosave'),
]
