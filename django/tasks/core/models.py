from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return (f'{self.title} - '
                f'{self.date.strftime("%d-%m-%y, %H:%M")}' + '\n'
                + f'{self.description}')
