from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy


class Collection(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    created = models.DateTimeField(default=timezone.now, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy(
            'log_collection_detail',
            kwargs={
                'slug': self.slug,
                'collection_pk': self.pk,
            },
        )


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(default=timezone.now, db_index=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Event(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.item.name
