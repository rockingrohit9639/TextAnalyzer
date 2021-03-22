from django.db import models

class User_profile(models.Model):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=100,null=True)

    def __str__(self):
        return str(self.name)


