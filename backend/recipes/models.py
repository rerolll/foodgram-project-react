from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tags(models.Model):
    id = models.TextField
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    id = models.TextField
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recip(models.Model):
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    text = models.TextField
    ingredients = models.ManyToManyField(Ingredients)
    tags = models.ManyToManyField(Tags)
    cooking_time = models.IntegerField()
    
    def __str__(self):
        return self.name