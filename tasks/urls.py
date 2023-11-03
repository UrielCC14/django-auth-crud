from django.urls import path
from . import views
urlpatterns = [
    path('',views.Home, name='home'),
    path('signup/',views.SignUp,name='signup'),
    path('task/',views.Tasks,name="task"),
    path('task/completed',views.Tasks_Completed,name="task_completed"),
    path('logout/',views.signout,name='logout'),
    path('signin/',views.SignIn,name='signin'),
    path('task/create/',views.Create_Task,name='task_create'),
    path('task/detail<int:id>/',views.Task_Detail,name='detail'),
    path('task/detail<int:id>/complete',views.Task_Complete,name='task_complete'),
    path('task/detail<int:id>/delete',views.Task_Delete,name='task_delete'),
]