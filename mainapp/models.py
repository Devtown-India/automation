from django.db import models



class sentInvitation(models.Model):
    name=models.CharField(max_length=100)
    headline=models.CharField(max_length=1000)
    location=models.CharField(max_length=500)
    headings=models.CharField(max_length=1000)
    highlights=models.CharField(max_length=1000)
    summary=models.CharField(max_length=1000)
    activity=models.CharField(max_length=2000)
    education=models.CharField(max_length=2000)
    skills=models.CharField(max_length=2000)
    interests=models.CharField(max_length=2000)
    url=models.CharField(max_length=300)

    def __str__(self):
        return self.name