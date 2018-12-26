from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=50)

    # objects = models.Manager()

    def __str__(self):
        return str(self.name)

class oid(models.Model):
    url = models.CharField(max_length=200)
    bucket_name = models.CharField(max_length=100)
    object_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.bucket_name) + "/" + str(self.object_name)

class Image(models.Model):
    image_name = models.CharField(max_length=100)
    image_oid = models.ForeignKey(oid, on_delete=models.CASCADE)
    preview_url = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(Users,on_delete=models.SET_NULL, related_name="Users", null=True)
    is_private = models.BooleanField(default=False)
    pub_date = models.DateField(null=True)

    # objects = models.Manager()

    def __str__(self):
        return str(self.image_name)


