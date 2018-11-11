import weasyprint

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import View, UpdateView, ListView
from django.utils import timezone
from django.template import loader
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist

from api.models import Lexique
from api.models import FoireAuxQuestions
from api.models import Fanfic
from api.models import Chapter
from api.models import Board
from api.models import Topic
from api.models import Message
from api.models import AccountProfile

from markdownx.utils import markdownify

from api.helpcenter.forms import NewTopicForm, ReplyMessageForm

# Create your views here.
def browse_by_title(request, initial=None):
    if initial:
        words = Lexique.objects.filter(title__istartswith=initial).order_by('title')
    else:
        words = Lexique.objects.all().order_by('title')

    return render(request, 'help/dico.html', {
        'words': words,
        'initial': initial,
    })


class SearchSubmitView(View):
    template = 'help/search_submit.html'
    response_message = 'Search'

    def post(self, request):
        template = loader.get_template(self.template)
        query = request.POST.get('search', '')
        words = Lexique.objects.all().order_by('title')
        items = Lexique.objects.filter(title__icontains=query)
        context = {'title': self.response_message, 'query': query, 'items': items, 'words': words}
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template, content_type='text/html')


class SearchAjaxSubmitView(SearchSubmitView):
    template = 'help/search_results.html'
    response_message = ''


questions = FoireAuxQuestions.objects.all().order_by('libelle')
def foire_aux_questions_view(request):
    for question in questions:
        question.reponse = markdownify(question.reponse)
    return render(request, 'help/faq.html', {'questions': questions})


class CommunitiesListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'help/forum/communities.html'


def communities_view_board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('messages') - 1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'help/forum/topics.html', {'board': board, 'topics': topics})


@login_required(login_url=reverse_lazy('index'))
def communities_view_new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            Message.objects.create(
                text=form.cleaned_data.get('text'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topic_message', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'help/forum/new_topic.html', {'board': board, 'form': form})


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'help/forum/messages.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.messages.order_by('created_at')
        return queryset


@login_required(login_url=reverse_lazy('index'))
def communities_view_topic_messages_reply(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.topic = topic
            message.created_by = request.user
            message.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('board_topic_message', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_message_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=message.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_message_url)
    else:
        form = ReplyMessageForm()
    return render(request, 'help/forum/reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class MessageUpdateView(UpdateView):
    model = Message
    fields = ('text',)
    template_name = 'help/forum/edit_message.html'
    pk_url_kwarg = 'message_pk'
    context_object_name = 'message'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.updated_by = self.request.user
        message.updated_at = timezone.now()
        message.save()
        return redirect('board_topic_message', pk=message.topic.board.pk, topic_pk=message.topic.pk)



def fanfic_pdf(request, fanfic_id):
    """
    Generate pdf output
    """
    try:
        fanfic = Fanfic.objects.filter(status="publié").get(id=fanfic_id)
        chapters = Chapter.objects.filter(fanfic=fanfic, status="publié")
        html = render_to_string('pdf/fanfic.html', {'fanfic': fanfic, 'chapters': chapters})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="fanfic_{}.pdf"'.format(fanfic.id)
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/styles/base.css')])
        return response
    except ObjectDoesNotExist:
        raise Http404("Cette fanfiction n'existe pas")
