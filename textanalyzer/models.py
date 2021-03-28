from django.db import models

class User_profile(models.Model):
    name = models.CharField(max_length=200, default="", blank=True)
    email = models.EmailField(max_length=100, default="", blank=True)
    message=models.TextField(default="",blank=True)

    def __str__(self):
        return str(self.name)

class Pdf(models.Model):
    name = models.CharField(max_length=200)
  
    def __str__(self):
        return self.name

