from django.urls import path,include
from .views import *
urlpatterns = [
    path('',registration,name='registration'),
    path('userlogin/',userlogin,name='userlogin'),
    path('homepage/',homepage,name='homepage'),
    path('participant/',participant,name='participant'),
    path('addParticipant/',addParticipant,name='addParticipant'),    
    path('editParticipant/<int:my_id>',editParticipant,name='editParticipant'),
    path('deleteParticipant/<int:my_id>',deleteParticipant,name='deleteParticipant'),
    path('addOption/',addOption,name='addOption'),    
    path('editQuiz/<int:id>',editQuiz,name='editQuiz'),
    path('deleteQuiz/<int:id>',deleteQuiz,name='deleteQuiz'),
    path('addQuestion/',addQuestion,name='addQuestion'),
    path('addQuiz/',addQuiz,name='addQuiz'),
    path('quizDetails/<int:id>',quizDetails,name='quizDetails'),
    path('user_logout/',user_logout,name='user_logout')
]