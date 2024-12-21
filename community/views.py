from django.shortcuts import render, get_object_or_404
from .models import Post, Category

# Create your views here.
def community_list(request):
    categories = Category.objects.all()
    posts = Post.objects.all()

    context = {
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'community/community_list.html', context)
