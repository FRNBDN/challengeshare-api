from django.urls import path
from submissions import views

urlpatterns = [
    path('submissions/', views.SubmissionList.as_view()),
    path('submissions/<int:pk>', views.SubmissionDetail.as_view()),
]
