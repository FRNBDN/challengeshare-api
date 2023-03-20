from django.urls import path
from challengefollowers import views

urlpatterns = [
    path('cfollowers/', views.ChallengeFollowerList.as_view()),
    path('cfollowers/<int:pk>', views.ChallengeFollowerDetail.as_view()),
]
