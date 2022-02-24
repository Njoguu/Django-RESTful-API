from django.db import models

# Create your models here.
class developers(models.Model):
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)
    email = models.EmailField()
    github_username = models.CharField(max_length=15)
    stacks = models.TextField()

    def __str__(self):
        return self.fname
