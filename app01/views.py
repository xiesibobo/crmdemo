import json
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.db import transaction
# Create your views here.
from app01 import models, forms, modelforms


def login(request):
    if request.method == "POST":

        user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            auth.login(request, user)

            return redirect('/questionnairemanage/')
    return render(request, 'login.html')


def questionnairemanage(request):
    questionnaire_list = models.Questionnaire.objects.filter(creator=request.user)
    return render(request, 'questionnairemanage.html', {'questionnaire_list': questionnaire_list})


def test(request):
    obj_list = models.UserInfo.objects.values()
    print(obj_list)
    return HttpResponse('OK!')


def questionnaireadd(request):
    if request.method == 'POST':
        questionnaireform = forms.QuestionnaireForm(request=request, data=request.POST)
        if questionnaireform.is_valid():
            obj = models.Questionnaire.objects.create(
                title=questionnaireform.cleaned_data.get('title'),
                creator_id=questionnaireform.cleaned_data.get('creator'),
                cls_id=questionnaireform.cleaned_data.get('cls')
            )

            # return redirect('/questionnairemanage/')
            return HttpResponse(json.dumps(questionnaireform.cleaned_data))
    questionnaireform = forms.QuestionnaireForm(request=request)
    return render(request, 'questionnaireaadd.html', {'questionnaireform': questionnaireform})


def questionnaireedit(request, clsid, qsnreid):
    if request.is_ajax():
        questions = json.loads(request.POST.get('quetions'))
        print(questions)
        with transaction.atomic():
            for question in questions:
                # 创建或更新问题
                qustion_id = question.get('qustion_id')
                tp_id = question.get('tp')
                qtitle = question.get('title')
                qsform = forms.QuestionsForm({'title': qtitle, 'tp': tp_id})
                if qsform.is_valid():
                    if qustion_id:
                        qobj_set = models.Questions.objects.filter(id=qustion_id)
                        qobj_set.update(title=qtitle, tp=tp_id)
                        qobj = qobj_set.first()
                        if int(tp_id) != 2:
                            models.Option.objects.filter(qs=qobj).delete()
                    else:
                        qobj = models.Questions.objects.create(title=qtitle, tp=tp_id)
                    if int(tp_id) == 2 and question.get('options'):
                        bein = []
                        for option in question.get('options'):
                            # 创建或更新选项
                            if option.get('option_id') == 'new':

                                if option.get('title') and option.get('score'):
                                    optobj = models.Option.objects.create(title=option['title'], score=int(option['score']),
                                                                          qs=qobj)
                                    bein.append(optobj.id)
                            else:
                                option_id = option.get('option_id')
                                bein.append(int(option_id))
                                optobj = models.Option.objects.filter(id=option_id)
                                if optobj and option.get('title') and option.get('score'):
                                    optobj.update(title=option['title'], score=int(option['score']))
                        models.Option.objects.exclude(id__in=bein).delete()
                        # 删除已经不属于该问题的选项
            else:
                return HttpResponse(json.dumps({'flag': True, 'msg': '成功'}))
        return HttpResponse(json.dumps({'flag': False, 'msg': '请检查'}))

    def get_question():
        questions_list = models.Questions.objects.filter(naire_id=qsnreid)
        s = {'form': None, 'obj': None, 'option_class': 'hide', 'options': None}
        if not questions_list:
            s['form'] = forms.QuestionsForm()
            yield s
        else:
            for question in questions_list:
                s = {'form': None, 'obj': None, 'option_class': 'hide', 'options': None}

                def get_options():
                    option_list = models.Option.objects.filter(qs=question)
                    for option in option_list:
                        item = forms.OptionForm({'title': option.title, 'score': option.score})
                        yield {'item': item, 'obj': option}

                s['form'] = forms.QuestionsForm({'title': question.title, 'tp': question.tp})
                s['obj'] = question
                if question.tp == 2:
                    s['options'] = get_options()
                    s['option_class'] = ''
                yield s

    # result = {'question_form': get_question()}
    # for i in result['question_form']:
    #     print(i['form'])
    return render(request, 'questionnaireaedit.html', {'result': get_question(), 'cls': clsid, 'qsnreid': qsnreid})


def questionnaireedit2(request, clsid, qsnreid):
    def inner():
        que_list = models.Questions.objects.filter(naire_id=qsnreid)
        if not que_list:
            form = modelforms.QuestionsModelForm()
            yield {'form': form, 'obj': None, 'option_class': 'hide', 'options': None}

        else:
            for que in que_list:
                form = modelforms.QuestionsModelForm(instance=que)
                temp = {'form': form, 'obj': None, 'option_class': 'hide', 'options': None}
                if que.tp == 2:
                    temp['option_class'] = ''

                    def inneroption():
                        option_list = models.Option.objects.filter(qs=que)
                        for option in option_list:
                            yield {'item': modelforms.OptionModelForm(instance=option), 'obj': option}

                    temp['options'] = inneroption()
                yield temp

    return render(request, 'questionnaireaedit2.html', {'form': inner()})
