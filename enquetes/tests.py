from asyncio import futures
from audioop import reverse
import datetime
from nturl2path import url2pathname
from urllib import response
from venv import create
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from pyrsistent import s
from soupsieve import select

from .models import Question

def create_question(question_text, days):
    """
    Cria uma questão com um texto e um númerod e dias, o qual pode
    ser positivo ou negativo, contados a partir do dia corrente
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text= question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Se não existirem questões é exibida uma mensagem específica
        """
        response = self.client.get(reverse('enquetes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Nenhuma questão disponível")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        """
        Questões com a data de publicação no passado são exibidas na index
        """
        create_question(question_text='Questão no passado.', days=-30)
        response = self.client.get(reverse('enquetes:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Questão no passado>'])

    def test_future_question(self):
        """
        Questões com data de publicação no futuro não são exibidas na index
        """
        create_question(question_text="Questão no futuro", days=30)
        response = self.client.get(reverse('enquetes:index'))
        self.assertContains(response,"Nenhuma questão disponível.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        """
        Apenas questões com data de publicação no passado são exibidas
        """
        create_question(question_text="Questões no passado.", days=30)
        create_question(question_text="Questão no futuro.",days=30)
        response = self.client.get(reverse('enquetes:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Questões no passado>'])

    def test_two_past_questions(self):
        """
        São exibidas mais de uma questão com datas de publicação no passado
        """
        create_question(question_text="Questão no passado 1.", days=30)
        create_question(question_text="Questão no passado 2.", days=-5)
        response = self.client.get(reverse('enquetes:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
            ['<Question: Questão no passado 2.>', 
            '<Question: Questão no passado 1.>'])

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_old_question(self):
        """
        O método was_published_recently deve retornar False para 
        questões com data de publicação mais antiga que um dia
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds= 1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        """
        O método was_published_recently() deve retornar False para
        questões com data de publicação no futuro
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(),False)
    
    def test_was_published_recently_with_recent_question(self):
        """
        O método was_published_recently deve retornar True para 
        questões com data de publicação inferior a um dia
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds= 1)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionDetailsView(TestCase):
    def test_future_question(self):
        """
        Deverá retornar um erro 404 para questões com data no futuro
        """
        future_question = create_question(question_text="Questão no futuro.",days=5)
        url = reverse('enquetes:details', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """
        Deverá exibir corretamente as questões com data no passado
        """
        past_question = create_question(question_text="Questão no passado.",days=-5)
        url = reverse('enquetes:details', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)