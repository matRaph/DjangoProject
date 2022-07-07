from django.urls import path
from . import views

app_name = 'enquetes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path(
        'enquetes/<int:pk>/', views.DetailsView.as_view(), name='detalhes'
    ),

    path(
        'enquetes/<int:pk>/resultado/', views.ResultsView.as_view(), name='resultado'
    ),

    path(
        'enquetes/<int:question_id>/votacao/', views.vote, name='votacao'
    ),
]
