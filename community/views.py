from django.shortcuts import render, get_object_or_404
from .models import Post, Category

# Create your views here.
def community_list(request):
    categories = Category.objects.all()

    category_id = request.GET.get('category', None)
    
    if category_id:
        posts = Post.objects.filter(category__id=category_id)
    else:
        posts = Post.objects.all()

    context = {
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'community/community_list.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    context = {
        'post': post,
    }
    return render(request, 'community/post_detail.html', context)
