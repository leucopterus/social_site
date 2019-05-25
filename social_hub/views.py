from django.shortcuts import render
from django.db.models import Q
from common_user.models import CommonUser
from my_post.models import Post
from my_group.models import Group


def search_view(request):
    query = request.GET.get('q')
    result_user = []
    result_group = []
    result_post = []
    if query:
        user_lookups = Q(user__first_name__icontains=query) | Q(
            user__last_name__icontains=query) | Q(about__icontains=query)
        post_lookups = Q(text__icontains=query)
        group_lookups = Q(name__icontains=query) | Q(
            description__icontains=query)
        qs_user = CommonUser.objects.filter(user_lookups).distinct()
        qs_post = Post.objects.filter(post_lookups)
        qs_group = Group.objects.filter(group_lookups)
        result_user = qs_user
        result_post = qs_post
        result_group = qs_group
    context = {
        'users': result_user,
        'posts': result_post,
        'groups': result_group,
        'q': query,
    }
    return render(request, 'search.html', context)
