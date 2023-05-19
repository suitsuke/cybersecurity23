from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

#unsafe imports
import sqlite3

from .models import Choice, Question

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/polls/')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            return render(request, 'polls/login.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'polls/login.html')

@login_required
def index(request):
    
    

    search_query = request.GET.get('search')
    latest_question_list = []
    #this is what is written in the search text window
    
    if search_query:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        #insertion = alla oleva
        cursor.execute("SELECT id, question_text FROM polls_question WHERE question_text LIKE '%" + search_query + "%'").fetchall()
        rows = cursor.fetchall()
        for row in rows:
            question_id = row[0]
            question_text = row[1]
            question = Question(id=question_id, question_text=question_text)
            latest_question_list.append(question)

        conn.close()
    else:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]


    
    #######        a safer way to search questions     ########
    
    #if search_query:
    #    latest_question_list = Question.objects.filter(question_text__icontains=search_query)
    #else:
    #    latest_question_list = Question.objects.all()
    
    ######              end      ####### 

    if not search_query:
        latest_question_list = Question.objects.all()

    context = {'latest_question_list': latest_question_list, 'search': search_query}
    

    return render(request, 'polls/index.html', context) 

    

def admin(request):
    return render(request, )

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


@csrf_exempt
def vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message":"You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

