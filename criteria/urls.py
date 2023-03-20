from django.urls import path
from criteria import views

urlpatterns = [
    path('criteria/', views.CriteriaList.as_view()),
    path('criteria/<int:pk>/', views.CriteriaDetail.as_view()),
]