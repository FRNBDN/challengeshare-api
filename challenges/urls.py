from django.urls import path
from challenges import views

urlpatterns = [
    path('challenges/', views.ChallengesList.as_view()),
    path('challenges/<int:pk>', views.ChallengeDetail.as_view()),
]