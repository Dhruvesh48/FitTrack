from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    comment_form = CommentForm()

    if request.method == "POST":
        if 'add_comment' in request.POST:
            # Handle adding a comment
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, "Your comment has been added.")
                return redirect('post_detail', post_id=post.id)

        elif 'edit_comment' in request.POST:
            # Handle editing a comment
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id, author=request.user)
            edit_form = CommentForm(request.POST, instance=comment)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "Your comment has been updated.")
                return redirect('post_detail', post_id=post.id)

        elif 'delete_comment' in request.POST:
            # Handle deleting a comment
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            
            if comment.author == request.user or request.user.is_superuser:
                comment.delete()
                messages.success(request, "The comment has been deleted.")
            else:
                messages.error(request, "You do not have permission to delete this comment.")
            
            return redirect('post_detail', post_id=post.id)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'on_community_page': True
    }
    return render(request, 'community/post_detail.html', context)

