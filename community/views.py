from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from .forms import CommentForm

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
    comments = post.comments.all()
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'community/post_detail.html', context)
