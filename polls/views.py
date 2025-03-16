from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question,Pirvate_Question,Pirvate_Choice
from django.http import Http404
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions and categorize them.
        """
        questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

        for question in questions:
            # Calculate total votes for each question
            total_votes = sum(choice.votes for choice in question.choice_set.all())
            question.total_votes = total_votes

        return questions


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
class pirvate_polls(generic.ListView):
        template_name = "polls/pirvate_poll.html"
        context_object_name = "latest_question_list"

        def get_queryset(self):
            """
            Return the last five published questions and categorize them.
            """
            questions = Pirvate_Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

            return questions

class PirvateDetailView(generic.DetailView):
    model = Pirvate_Question
    template_name = "polls/pirvate_detail.html"
    context_object_name = 'question'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Pirvate_Question.objects.filter(pub_date__lte=timezone.now())


class PirvateResultsView(generic.DetailView):
    model = Pirvate_Question
    template_name = "polls/pirvate_results.html"
    context_object_name = 'question'

def pivate_vote(request, question_id):
    question = get_object_or_404(Pirvate_Question, pk=question_id)
    try:
        # ดึงตัวเลือกที่เกี่ยวข้องกับ Pirvate_Question
        selected_choice = question.pirvate_choice_set.get(pk=request.POST["choice"])
    except (KeyError, Pirvate_Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/pivate_detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # Redirect ไปยังผลลัพธ์ของ private polls (คุณอาจต้องปรับชื่อ URL ด้วยถ้าจำเป็น)
        return HttpResponseRedirect(reverse("polls:pivateresults", args=(question.id,)))