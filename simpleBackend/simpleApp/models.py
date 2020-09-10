from djongo import models


# Create your models here.

class Posts(models.Model):
    id = models.ObjectIdField()
    name = models.CharField(max_length=225)
    loc = models.JSONField()
    objects = models.DjongoManager()

    
