from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from chapters.api.serializers import ChapterSerializer, ChapterFormattedSerializer

from chapters.models import Chapter

from api import custompagination

import logging
import openai

logger = logging.getLogger(__name__)


class ChapterBaseAPIView(generics.GenericAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create_or_update(self, serializer):
        serializer.save(author=self.request.user)


class ChapterListApiView(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterFormattedSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    pagination_class = custompagination.StandardResultsSetPagination
    filter_fields = (
        'status',
    )

    def get_queryset(self):
        fanfic_id = self.request.query_params.get('fanfic', None)
        if fanfic_id is None:
            raise NotFound('No fanfic id provided')
        return Chapter.objects.filter(fanfic=fanfic_id)


class ChapterCreateApiView(ChapterBaseAPIView, generics.CreateAPIView):
    throttle_classes = [UserRateThrottle,]
    def perform_create(self, serializer):
        self.perform_create_or_update(serializer)




class ChapterDetailView(ChapterBaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    name = 'chapter-detail'

    def get_queryset(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return Chapter.objects.filter(author=self.request.user)
        return Chapter.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save(author=self.request.user)
        instance.full_clean()
        self.perform_create_or_update(serializer)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_styles_prompts(request):
    styles = ['neutre', 'romantique', 'dramatique', 'comique','mystérieux']
    return Response(styles)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_chapter_summary(request):
    prompt = request.data.get('prompt', '')
    style = request.data.get('style', 'neutre')

    styles = {
        'neutre': 'avec un ton neutre et équilibré',
        'romantique': 'avec un ton romantique et poétique',
        'dramatique': 'avec une intensité dramatique',
        'comique': 'avec un ton humoristique',
        'mystérieux': 'avec une ambiance inquétante',
    }

    prompt_style = styles.get(style, 'avec un ton neutre et équilibré')
    system_message = f"Tu es un écrivain de fanfiction expert. Ecris {prompt_style}""'"

    response = openai.Completion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        max_tokens=600,
    )

    return Response({
        'generated_summary': response["choices"][0]["message"]["content"],
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def autosave_chapter(request, fanfic):
    data_rq = request.data
    chapter, created = Chapter.objects.update_or_create(
        author=request.user,
        fanfic=fanfic,
        title=data_rq['title'],
        description=data_rq['description'],
        text=data_rq['text'],
        order=data_rq['order'],
        status=data_rq['status'],
    )
    return Response({
        'message': 'Autosaved',
        'id': chapter.id,
        'created': created,
        'updated': chapter.updated,
        'published': chapter.published,
        'is_published': chapter.is_published,
        'fanfic': chapter.fanfic.title,
        'title': chapter.title,
        'description': chapter.description,
        'text': chapter.text,
        'order': chapter.order,
        'status': chapter.status,
        'author': chapter.author.username,
        'fanfic_id': chapter.fanfic.id,
        'author_id': chapter.author.id,
    })
