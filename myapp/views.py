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
            
            # user.set_password(form.cleaned_data.get('password1'))
            user.save()
            if user.user_type == 'admin':
                admin = Admin.objects.create(user=user)
                admin.save()
            else:
                participant = Participant.objects.create(user=user)
                participant.save()
            
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
                return redirect('editProfile')
    else:
        form = LoginForm()

    return render(request,'loginForm.html',{'form':form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('registration')

    
@login_required
def dashboard(request):
    quizzes = Quiz.objects.all()
    isAdmin = Admin.objects.filter(user=request.user).exists()
    
    profile = None
    results = []
    if isAdmin:
        profile = Admin.objects.get(user=request.user)
    else:
        profile = Participant.objects.get(user=request.user)
        results = QuizResult.objects.filter(participant=profile)

    return render(request, 'dashboard.html', {
        'quizzes': quizzes,
        'isAdmin': isAdmin,
        'profile': profile,
        'results': results
    })

@login_required
def editProfile(request):
    # user = CustomUser.objects.get(user=request.user)
    # if user.user_type == 'admin':
    #     profile = Admin.objects.get(user=request.user)
    #     ProfileForm = AdminForm
    # else:
    #     profile = Participant.objects.get(user=request.user)
    #     ProfileForm = ParticipantForm

    isAdmin = Admin.objects.filter(user=request.user).exists()
    
    if isAdmin:
        profile = Admin.objects.get(user=request.user)
        if request.method == 'POST':
            
            form = AdminForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = AdminForm(instance=profile)
        
        return render(request, 'editProfile.html', {'form': form})
    else:
        profile = Participant.objects.get(user=request.user)
        if request.method == 'POST':
            
            form = ParticipantForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = ParticipantForm(instance=profile)
        
        return render(request, 'editProfile.html', {'form': form})

    # if request.method == 'POST':
        
    #     form = ProfileForm(request.POST, instance=profile)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('dashboard')
    # else:
    #     form = ProfileForm(instance=profile)

    # return render(request, 'editProfile.html', {'form': form})

@login_required
def addQuiz(request):
    admin = get_object_or_404(Admin, user=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.admin = admin
            quiz.save()
            return redirect('dashboard')
    else:
        form = QuizForm()
    return render(request, 'addQuiz.html', {'form': form})

@login_required
def addQuestion(request):
    admin = get_object_or_404(Admin, user=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.admin = admin
            quiz.save()
            return redirect('dashboard')
    else:
        form = QuestionForm()
    return render(request, 'addQuestion.html', {'form': form})


@login_required
def addOption(request):
    admin = get_object_or_404(Admin, user=request.user)
    if request.method == "POST":
        form =OptionForm(request.POST,request.FILES)
        if form.is_valid():
            quiz=form.save(commit=False)
            quiz.admin = admin
            quiz.save()
            return redirect('dashboard')
    else:
        form = OptionForm()
    return render(request,'addOption.html',{'form':form})

@login_required
def editQuiz(request,id):
    quiz = Quiz.objects.get(id=id)
    if request.method == "POST":
            form = QuizForm(request.POST,instance=quiz)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    else:
        form = QuizForm(quiz)
    return render(request,'editQuiz.html',{'form':form})

@login_required
def editQuestion(request,id):
    question = Question.objects.get(id=id)
    if request.method == "POST":
            form = QuestionForm(request.POST,instance=question)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    else:
        form = QuestionForm(question)
    return render(request,'editQuestion.html',{'form':form})



@login_required
def editOption(request,id):
    option = Option.objects.get(id=id)
    if request.method == "POST":
        form = OptionForm(request.POST,instance=option)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = OptionForm(option)
    return render(request,'editOption.html',{'form':form})

@login_required
def deleteQuiz(request,id):
    quiz = Quiz.objects.get(id=id)
    quiz.delete()
    return redirect('deleteQuiz')



@login_required
def deleteQuestion(request,id):
    question = Question.objects.get(id=id)
    question.delete()
    return redirect('deleteQuestion')

@login_required
def deleteQuiz(request,id):
    option = Option.objects.get(id=id)
    option.delete()
    return redirect('deleteOption')

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
def take_quiz(request, id):

    participant = get_object_or_404(Participant, user = request.user)

    quiz = Quiz.objects.get(id=id)

    if request.method == "POST":
        score = 0
        questions = quiz.questions.all()
        for question in questions:
            selected_option_id = request.POST.get(f"question_{question.id}")

            if selected_option_id:
                correct = question.options.filter(
                    id=selected_option_id,
                    is_correct=True
                ).exists()

                if correct:
                    score += 1

        return redirect("take_quiz",id=quiz.id)

    questions = quiz.questions.order_by("?")
    question_data = []

    for question in questions:
        options = question.options.order_by("?")

        question_data.append({"question": question,"options": options})
    print(question_data)

    return render(request,'quiz.html',
        {
            "quiz": quiz,
            "question_data": question_data
        }
    )

@login_required
def result_view(request, id):
    
    participant = get_object_or_404(Participant, user = request.user)

    quiz = get_object_or_404(Quiz, id = id)

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
            'result':result,
            'position':position
        }
    )

@login_required
def quizDetails(request,id):
    questions = Question.objects.filter(quiz__id=id)
    context = {
        'questions' : questions
    }
    return render(request,'quizDetails.html',context)

    