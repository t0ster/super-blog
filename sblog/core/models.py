from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('post', args=[str(self.id)])

    def __unicode__(self):
        return self.title


class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images')
    image = models.ImageField(upload_to='images', blank=True)
