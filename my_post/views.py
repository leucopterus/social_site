from django.shortcuts import render
from django.views import generic
from .models import Post
# Create your views here.


class PostDetailView(generic.DetailView):
    context_object_name = 'post_details'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_number'] = self.kwargs['pk']
        return context


class PostCreateView(generic.CreateView):
    pass


class PostUpdateView(generic.UpdateView):
    pass


class PostDeleteView(generic.DeleteView):
    pass
