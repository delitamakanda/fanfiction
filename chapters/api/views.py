import logging

from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam
)
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from api import custompagination
from chapters.api.serializers import ChapterSerializer, ChapterFormattedSerializer, ChapterSummaryRequestSerializer, \
    ChapterSummaryResponseSerializer
from chapters.models import Chapter

client = OpenAI(api_key=settings.OPENAI_API_KEY)

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


@extend_schema(
	summary='List all styles prompts',
	description="List all available styles prompts for the chapters.",
    responses={
        200: OpenApiResponse(
			description="List of styles prompts",
                response=OpenApiExample(
					name="Styles",
                    value=list(),
                ),
		),
        403: OpenApiResponse(
            description="Forbidden",
        )
	},
    tags=['Chapters'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_styles_prompts(request):
    styles = ['neutre', 'romantique', 'dramatique', 'comique','mystérieux']
    return Response(styles)


@extend_schema(
    summary="generate chapter summary",
    description="Generate a summary for a given chapter.",
    request=ChapterSummaryRequestSerializer,
    responses={
        200: ChapterSummaryResponseSerializer,
    },
    examples=[
        OpenApiExample(
            name="Neutre",
            value={
                "prompt": "Le château est une maison, et il est en plein jour.",
                "style": "neutre",
            },
        )
    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_chapter_summary(request):
    serializer = ChapterSummaryRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    prompt = serializer.validated_data['prompt']
    style = serializer.validated_data.get('style', 'neutre')

    system_message = f"""
    Tu es un auteur expert de fanfiction expert.
    Style demandé : {style}.
    Ecris un texte immersif, mature et cohérent.
    """

    messages: list[ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam] = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.9,
            max_tokens=600,
            messages=messages
        )

        return Response({
            'generated_summary': response.choices[0].message.content,
        })
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response({
            'error': str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@extend_schema(
	summary='Autosave a chapter',
    description="Allow users to autosave their chapters.",
    parameters=[
        OpenApiParameter(
            name='fanfic',
			description='Fanfic ID',
            type=int,
            required=True,
        ),
    ],
    responses={
        200: ChapterSerializer,
        403: OpenApiResponse(
            description="Forbidden",
        ),
        404: OpenApiResponse(
            description="Fanfic not found",
        ),
        400: OpenApiResponse(
            description="Bad request",
        ),
        500: OpenApiResponse(
            description="Internal server error",
        )
    },
    tags=['Chapters'],
)
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
