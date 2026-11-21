from django.urls import path,include
from .views import *
urlpatterns = [
    path('',registration,name='registration'),
    path('userlogin/',userlogin,name='userlogin'),
    path('homepage/',homepage,name='homepage'),
    path('dashboard/',dashboard,name='dashboard'),
    path("editProfile/",editProfile,name="editProfile"),    
    path('editProfile/<int:id>',editProfile,name='editProfile'),
    path('result/<int:quiz_id>/',result_view,name='result'),
    path('addOption/',addOption,name='addOption'),    
    path('editQuiz/<int:id>',editQuiz,name='editQuiz'),
    path('deleteQuiz/<int:id>',deleteQuiz,name='deleteQuiz'),
    path('addQuestion/',addQuestion,name='addQuestion'),
    path('addQuiz/',addQuiz,name='addQuiz'),
    path('take_quiz/<int:id>',take_quiz,name='take_quiz'),
    path("result/<int:id>/",result_view,name="result"),
    path('quizDetails/<int:id>',quizDetails,name='quizDetails'),
    path('user_logout/',user_logout,name='user_logout')
]