from django.urls import path
from uploads import views

urlpatterns = [
    path('uploads/', views.UploadList.as_view()),
    path('uploads/<int:pk>', views.UploadDetail.as_view()),
]