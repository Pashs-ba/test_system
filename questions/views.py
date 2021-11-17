from django.shortcuts import render, redirect
from core.models import Question, QuestionAns, Competitions
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def question(request, pk, ret):
    question = Question.objects.get(pk=pk)
    user = request.user

    if request.method == 'POST':
        ans = json.loads(question.question)
        if question.type == '0':
            QuestionAns(user=user,
                        question=question,
                        result=ans['ans'].lower() == request.POST['ans'].lower()).save()
        elif question.type == '1':
            for i in ans['ans']:
                if ans['ans'][i][1]:
                    QuestionAns(user=user,
                                question=question,
                                result=request.POST['ans'] == i).save()
        elif question.type == '2':
            for i in ans['ans']:
                if ans['ans'][i][1] and not request.POST.get(i):
                    print('some')
                    QuestionAns(user=user,
                                question=question,
                                result=False).save()
                    break
            else:
                print('eles')
                QuestionAns(user=user,
                            question=question,
                            result=True).save()
        messages.success(request, 'Ответ записан')
        return redirect('competition_page', ret)
    else:
        answers = []
        print(json.loads(question.question))
        if json.loads(question.question)['type'] != 0:
            for i in json.loads(question.question)['ans']:
                answers.append([json.loads(question.question)['ans'][i][0], i])

        return render(request, 'question_page.html', {'question': question,
                                                      'answers': answers})

# Create your views here.
