from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Post, Comment

class CommunityViewsTest(TestCase):
    
    def setUp(self):
        """Create initial test data."""
        self.category = Category.objects.create(name="Test Category", description="A test category")
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="otheruser", password="password123")

        self.post = Post.objects.create(
            title="Test Post", 
            content="Test content", 
            author=self.user, 
            category=self.category
        )

        self.comment = Comment.objects.create(
            post=self.post, 
            author=self.user, 
            content="Test comment"
        )

    def test_community_list_view(self):
        """Test the community list view."""
        url = reverse('community_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/community_list.html')
        self.assertContains(response, self.post.title)

    def test_post_detail_view_authenticated(self):
        """Test the post detail view for authenticated users."""
        self.client.login(username='testuser', password='password123')

        url = reverse('post_detail', args=[self.post.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/post_detail.html')
        self.assertContains(response, self.post.title)

    def test_post_detail_view_unauthenticated(self):
        """Test that the post detail view redirects non-logged-in users to login page."""
        url = reverse('post_detail', args=[self.post.id])
        response = self.client.get(url)

        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_comment_permission(self):
        """Test that only the comment author or an admin can delete their comment."""

        self.client.login(username='testuser', password='password123')
        url = reverse('post_detail', args=[self.post.id])

        response = self.client.post(url, {'comment_id': self.comment.id, 'delete_comment': True}, follow=True)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
        self.assertContains(response, "The comment has been deleted.")

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Another test comment"
        )

        self.client.login(username='otheruser', password='password123')

        response = self.client.post(url, {'comment_id': self.comment.id, 'delete_comment': True}, follow=True)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())  # Should not be deleted by a non-author
        self.assertContains(response, "You do not have permission to delete this comment.")  # Ensure the error message is shown

        self.client.login(username='testuser', password='password123')
        self.user.is_superuser = True
        self.user.save()

        response = self.client.post(url, {'comment_id': self.comment.id, 'delete_comment': True}, follow=True)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())  # Should be deleted by a superuser
        self.assertContains(response, "The comment has been deleted.")  # Ensure the success message is shown


