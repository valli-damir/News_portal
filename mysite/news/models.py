from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self)
        comments_rating = Comment.objects.filter(user=self.authorUser)
        posts_comments_rating = Comment.objects.filter(post__author=self)

        print(posts_rating)
        print('-------------')
        print(comments_rating)
        print('-------------')
        print(posts_comments_rating)
        self.rating = posts_rating*3 + comments_rating + posts_comments_rating
        self.save()


        # posts = self.post_set.all()
        # for post in posts:
        #     post.rating = post.rating * 3

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):


    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_lenght=20)
    dataCreations = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # Метод preview() модели Post, который возвращает начало статьи (предварительный просмотр)
    # длиной 124 символа и добавляет многоточие в конце.

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
