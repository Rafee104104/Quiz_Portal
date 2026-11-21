from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
 
class CustomUser(AbstractUser):
    USER = [
        ('admin','Admin'),
        ('participant','Participant')
    ]
    user_type = models.CharField(max_length=50,choices= USER,null=True)
    def __str__(self):
        return self.username

class Admin(models.Model):
    #  Name Class Age gender Institution
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin',null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    age = models.PositiveIntegerField(null=True,blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True,blank=True)
    institution = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name

    
class Quiz(models.Model):
    admin = models.ForeignKey(Admin,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    admin = models.ForeignKey(Admin,on_delete=models.CASCADE,null=True,blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions',null=True,blank=True)
    question = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.quiz.title} - {self.question}"

class Option(models.Model):
    admin = models.ForeignKey(Admin,on_delete=models.CASCADE,null=True,blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options',null=True,blank=True)
    option = models.CharField(max_length=255,null=True,blank=True)
    is_correct = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.option



class Participant(models.Model):
    #  Name Class Age gender Institution
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='participant',null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    student_class = models.CharField(max_length=50,null=True,blank=True)
    age = models.PositiveIntegerField(null=True,blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True,blank=True)
    institution = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name



class QuizResult(models.Model):
    participant = models.ForeignKey(Participant,on_delete=models.CASCADE,related_name='participant',blank=True,null=True)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='participant',blank=True,null=True)
    score = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.name} - {self.quiz.title}"


