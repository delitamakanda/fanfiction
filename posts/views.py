from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views.generic.list import ListView

from posts.models import Post, Tag


@method_decorator(xframe_options_exempt, name='dispatch')
class PostsListView(ListView):
    queryset = Post.objects.order_by('-created')
    model = Post
    paginate_by = 4
    context_object_name = 'posts'
    template_name = 'post/notice.html'


def generate_fake_data(request):
    from model_mommy import mommy
    mommy.make('posts.Post', _quantity=30)
    return redirect('posts/list')
