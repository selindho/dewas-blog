from django.db import models

# Create your models here.


class BlogPost(models.Model):

    title = models.CharField(max_length=30)
    version = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField()
    content = models.TextField()

    @classmethod
    def getById(cls, id):
        try:
            return cls.objects.get(id=id)
        except:
            return None

    @classmethod
    def getAll(cls):
        try:
            return cls.objects.all()
        except:
            return None