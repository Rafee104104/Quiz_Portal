from django.shortcuts import render, redirect
from django.http import request
from .models import *
from django.contrib.auth import *
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def registration(request):
    if(request.method == "POST"):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password1'])
            # user.set_password(form.cleaned_data.get('password1')])
            user.save()
            return redirect('userlogin')
    else:
        form = RegistrationForm()
    return render(request,'registrationform.html',{'form':form})


def userlogin(request):
    if request.method=="POST":
        form = LoginForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
        
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('homepage')
    else:
        form = LoginForm()

    return render(request,'loginForm.html',{'form':form})

@login_required
def participant(request):

    participants =Participant.objects.all()

    context = {
        'participants' : participants
    }

    return render(request,'participant.html',context)

@login_required
def addParticipant(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('participant')
    else:
        form = ParticipantForm()
    return render(request,'addParticipant.html',{'form':form})


@login_required
def editParticipant(request,my_id):
    participant = Participant.objects.get(id=my_id)
    if request.method == "POST":
            form = ParticipantForm(request.POST,instance=participant)
            if form.is_valid():
                form.save()
                return redirect('participant')
    else:
        form = ParticipantForm()
    return render(request,'editParticipant.html',{'form':form})
@login_required
def deleteParticipant(request,my_id):
    participant = Participant.objects.get(id=my_id)
    participant.delete()
    return redirect('participant')
@login_required
def addQuiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = QuizForm()
    return render(request,'addQuiz.html',{'form':form})
@login_required
def editQuiz(request,id):
    quiz = Quiz.objects.get(id=id)
    if request.method == "POST":
            form = QuizForm(request.POST,instance=quiz)
            if form.is_valid():
                form.save()
                return redirect('homepage')
    else:
        form = QuizForm(quiz)
    return render(request,'editQuiz.html',{'form':form})
@login_required
def deleteQuiz(request,id):
    quiz = Quiz.objects.get(id=id)
    quiz.delete()
    return redirect('deleteQuiz')

@login_required
def addQuestion(request):
    if request.method == "POST":
        form =QuestionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = QuestionForm()
    return render(request,'addQuestion.html',{'form':form})
@login_required
def addOption(request):
    if request.method == "POST":
        form =OptionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = OptionForm()
    return render(request,'addOption.html',{'form':form})
@login_required
def homepage(request):

    quizs =Quiz.objects.all()
    # questions = Question.objects.all()
    # options = Option.objects.all() lagbe na

    context = {
        'quizs' : quizs
    }

    return render(request,'homepage.html',context)
@login_required
def quizDetails(request,id):
    questions = Question.objects.filter(quiz__id=id)
    context = {
        'questions' : questions
    }
    return render(request,'quizDetails.html',context)
@login_required
def user_logout(request):
    logout(request)
    return redirect('registration')
    