from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy


class Collection(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    created = models.DateTimeField(default=timezone.now, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # todo: remove ability to delete collections
    archived = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.name
    
    #def get_absolute_url(self):
    #    return reverse_lazy(
    #        'collection-detail',
    #        kwargs={
    #            'slug': self.slug,
    #            'pk': self.pk,
    #        },
    #    )
