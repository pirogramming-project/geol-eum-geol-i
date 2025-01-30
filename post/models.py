from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# 함께 걸어요 (게시글)
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="post_images/", null=True, blank=True)  # 게시글 이미지
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 날짜

    def __str__(self):
        return self.title

# 게시글 댓글 (인원 모집)
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 날짜

    def __str__(self):
        return f"Comment by {self.user.nickname} on {self.post.title}"

