from datetime import datetime
from pyexpat import model
from time import timezone
from turtle import ondrag
from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Data de publicação')
    def __str__(self):
        return self.question_text
    def was_publishec_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text