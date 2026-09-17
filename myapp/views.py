from django.shortcuts import get_object_or_404, render, redirect
from django.http import request
from .models import *
from django.contrib.auth import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

def result_view(request, quiz_id):
    
    participant = get_object_or_404(
        Participant,
        user = request.user
    )

    quiz = get_object_or_404(
        Quiz,
        id = quiz_id
    )

    result = QuizResult.objects.filter(
        participant=participant,
        quiz=quiz
    ).order_by("-submitted_at").first()

    if result is None:
        return redirect("dashboard")

    better_scores = QuizResult.objects.filter(
        quiz=quiz,
        score__gt = result.score
    ).values("participant").distinct().count()

    position = better_scores +1

    return render(
        request,
        "quiz.html",
        {
            'quiz':quiz,
            'result':quiz,
            'position':position
        }
    )

@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    if request.method == "POST":
        score = 0

        questions = quiz.questions.all()

        for question in questions:
            selected_option_id = request.POST.get(
                f"question_{question.id}"
            )

            if selected_option_id:
                correct = question.options.filter(
                    id=selected_option_id,
                    is_correct=True
                ).exists()

                if correct:
                    score += 1

        return redirect(
            "take_quiz",
            quiz_id=quiz.id
        )

    questions = quiz.questions.order_by("?")

    question_data = []

    for question in questions:
        options = question.options.order_by("?")

        question_data.append({
            "question": question,
            "options": options
        })

    return render(
        request,
        'quiz.html',
        {
            "quiz": quiz,
            "question_data": question_data
        }
    )

# def take_quiz(request,quiz_id):
#     quiz = Quiz.objects.get(id=quiz_id).all()
#     if request.method=="POST":
#         score = 0

#         questions = quiz.questions.all()

#         for question in questions:

#             selected_option_id = request.POST.get(
#                 f"question_{question.id}"
#             )

#             if selected_option_id:

#                 correct = question.options.filter(
#                     id = selected_option_id,
#                     is_correct = True
#                 ).exists()

#                 if correct:
#                     score += 1

#         QuizResult.objects.create(
#             participant = participant,
#             quiz = quiz,
#             score = score
#         )

#         return redirect(
#             "take_quiz",
#             quiz_id=quiz.id
#         )


#     questions = quiz.questions.order_by("?")

#     question_data = []

#     for question in questions:

#         options = question.options().order_by("?")

#         question_data.append({
#             "question" : question,
#             "options" : options
#         })

#     return render(request,'quiz.html',
#         {
#             "quiz" : quiz,
#             "question_data" : question_data
#         }
#     )

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
        form = ParticipantForm(instance=participant)
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
    