from ast import keyword
from http.client import HTTPResponse
from time import time
from urllib import request
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View

from .models import Question, Choice

class MyView(View):
    def get(self, request, *args, **kwargs):
        return HTTPResponse('Hello, World!')

class IndexView(generic.ListView):
    template_name = 'enquetes/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:25]

class DetailsView(generic.DetailView):
    model = Question
    template_name = 'enquetes/detalhes.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name ='enquetes/resultado.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detalhes.html', {'question':question, 'error_message':"Você não selecionou uma opção",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('enquetes:resultado', args=(question_id,)))
