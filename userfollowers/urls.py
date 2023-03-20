from django.urls import path
from userfollowers import views

urlpatterns = [
    path('ufollowers/', views.UserFollowerList.as_view()),
    path('ufollowers/<int:pk>', views.UserFollowerDetail.as_view()),
]
