from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

class Category(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='title_genre')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='title_category',
        blank=True,
        null=True
    )
    def __str__(self):
        #выводим name title 
        return self.name 
    #category  

class Review(models.Model):
    title = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='review_title')
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_author')
    score = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        #выводим текст review
        return self.text

# id,title_id,text,author,score,pub_date

     

class Comment(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='comment_review')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    text = models.TextField()
    pub_date = models.DateTimeField('date_created', auto_now_add=True)

    def __str__(self):
        return self.text


