from django.urls import path
from . import views

app_name = 'enquetes'
urlpatterns = [
    path('', views.index, name='index'),

    path(
        'enquetes/<int:question_id>/',
        views.details, name='detail'
    ),

    # ex.: resultado - /enquete/5/resultado/
    path(
        'enquetes/<int:question_id>/results/',
        views.results, name='results'
    ),

    # ex.: votação - /enquete/5/votacao/
    path(
        'enquetes/<int:question_id>/votacao/',
        views.vote, name='votacao'
    ),

]