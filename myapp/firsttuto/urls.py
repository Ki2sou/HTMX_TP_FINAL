from django.urls import path
from firsttuto import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('tasks/',views.TaskList.as_view(),name='task-list'),
    path('db_tasks/', views.TaskListDB.as_view(), name='db_tasks'),
    path('db_tasks_pag/', views.listing, name='db_tasks_pag'),
]

htmx_views=[
    path("check_username",views.check_username,name="check_username"),
    path("add_task", views.add_task, name="add_task"),
    path("supp_task/<int:id>", views.supp_task, name="supp_task"),
    path("edit_task/<int:id>", views.edit_task, name="edit_task"),
    path("task_detail/<int:id>", views.task_detail, name="task_detail"),
    path("toggle_task_subscription/<int:id>", views.toggle_task_subscription, name="toggle_task_subscription"),
    path("search-task/", views.search_task, name="search-task"),
]

urlpatterns += htmx_views
