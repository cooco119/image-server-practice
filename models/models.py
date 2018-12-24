from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=50)

    # objects = models.Manager()

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    image_name = models.CharField(max_length=100)
    image_oid = models.IntegerField(default=0)
    user = models.ForeignKey(Users,on_delete=models.SET_NULL, related_name="Users", null=True)
    is_private = models.BooleanField(default=False)

    # objects = models.Manager()

    def __str__(self):
        return str(self.image_name)

