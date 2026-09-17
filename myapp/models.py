from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
 
class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

class Quiz(models.Model):
    title = models.TextField(max_length=300,blank=True,null=True)
    description = models.TextField(max_length=300,blank=True,null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.DO_NOTHING,related_name='questions',blank=True,null=True)
    question =models.TextField(max_length=300,blank=True,null=True)

    def __str__(self):
        return self.question

class Option(models.Model):
     question = models.ForeignKey(Question,on_delete=models.DO_NOTHING,related_name='options',blank=True,null=True)
     option = models.TextField(max_length=300,blank=True,null=True)
     is_correct = models.BooleanField(default='false',blank=True,null=True)

     def __str__(self):
        return self.option

class Participant(models.Model):
    #  Name Class Age gender Institution
    Name = models.TextField(max_length=90,blank=True,null=True)
    Class = models.CharField(max_length=90,blank=True,null=True)
    Age = models.IntegerField(blank=True,null=True)
    Institution = models.TextField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.Name

class QuizResult(models.Model):
    participant = models.ForeignKey(Participant,on_delete=models.CASCADE,related_name='participant',blank=True,null=True)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='participant',blank=True,null=True)
    score = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)