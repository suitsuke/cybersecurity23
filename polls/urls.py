from django.urls import path

from . import views
#from .views import logout_view

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
