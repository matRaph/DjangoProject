from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('pub_date') [:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'index.html', context)

def details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'details.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'details.html',
        {'question': question,
         'error_message': "Você não selecionou uma opção"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('enquetes:results', args=(question_id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question':question})