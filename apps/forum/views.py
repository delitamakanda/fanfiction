"""Server-rendered forum pages (Django templates)."""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, UpdateView

from apps.forum import services
from apps.forum.forms import NewTopicForm, ReplyMessageForm
from apps.forum.models import MESSAGES_PER_PAGE, Board, Message, Topic


class CommunitiesListView(ListView):
    model = Board
    context_object_name = "boards"
    template_name = "forum/communities.html"


def communities_view_board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = (
        board.topics.select_related("starter")
        .order_by("-last_updated")
        .annotate(replies=Count("messages") - 1)
    )
    topics = Paginator(queryset, 20).get_page(request.GET.get("page"))
    return render(request, "forum/topics.html", {"board": board, "topics": topics})


@login_required
def communities_view_new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    form = NewTopicForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        topic = services.start_topic(
            board=board,
            starter=request.user,
            subject=form.cleaned_data["subject"],
            text=form.cleaned_data["text"],
        )
        return redirect("api:forum:board_topic_message", pk=pk, topic_pk=topic.pk)
    return render(request, "forum/new_topic.html", {"board": board, "form": form})


class MessageListView(ListView):
    context_object_name = "messages"
    template_name = "forum/messages.html"
    paginate_by = MESSAGES_PER_PAGE

    def get_queryset(self):
        self.topic = get_object_or_404(
            Topic.objects.select_related("board"),
            board__pk=self.kwargs["pk"],
            pk=self.kwargs["topic_pk"],
        )
        return self.topic.messages.select_related("created_by").order_by("created_at")

    def get_context_data(self, **kwargs):
        services.register_topic_view(self.topic, self.request.session)
        kwargs["topic"] = self.topic
        return super().get_context_data(**kwargs)


@login_required
def communities_view_topic_messages_reply(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    form = ReplyMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        message = services.reply(
            topic=topic, author=request.user, text=form.cleaned_data["text"]
        )
        topic_url = reverse(
            "api:forum:board_topic_message", kwargs={"pk": pk, "topic_pk": topic_pk}
        )
        return redirect(f"{topic_url}?page={topic.get_page_count()}#{message.pk}")
    return render(request, "forum/reply_topic.html", {"topic": topic, "form": form})


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ("text",)
    template_name = "forum/edit_message.html"
    pk_url_kwarg = "message_pk"
    context_object_name = "message"

    def get_queryset(self):
        return Message.objects.filter(
            created_by=self.request.user,
            topic__pk=self.kwargs["topic_pk"],
            topic__board__pk=self.kwargs["pk"],
        ).select_related("topic__board")

    def form_valid(self, form):
        message = services.edit_message(
            self.object, editor=self.request.user, text=form.cleaned_data["text"]
        )
        return redirect(
            "api:forum:board_topic_message",
            pk=message.topic.board.pk,
            topic_pk=message.topic.pk,
        )
