from django.db import models

class User(models.Model):
    uid = models.IntegerField(primary_key=True, serialize=True)
    name = models.CharField(max_length=50)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    image_id = models.IntegerField(default=0)   
    image_name = models.CharField(max_length=50)
    image_oid = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return str(self.image_name)

