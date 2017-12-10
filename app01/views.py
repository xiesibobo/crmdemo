import json
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.db import transaction
# Create your views here.
from app01 import models, forms, modelforms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

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
        flag=False
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
                                else:flag=True
                            else:
                                option_id = option.get('option_id')
                                bein.append(int(option_id))
                                optobj = models.Option.objects.filter(id=option_id)
                                if optobj and option.get('title') and option.get('score'):
                                    optobj.update(title=option['title'], score=int(option['score']))
                                else:
                                    flag=True
                        models.Option.objects.exclude(id__in=bein).delete()
                        # 删除已经不属于该问题的选项
                else:break
                if flag: break
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

#modelforms
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


# 填写问卷

from django.forms import Form
from django.forms import fields
from django.forms import widgets
#验证输入的长度
def func(val):
    if len(val) < 15:
        raise ValidationError('你太短了')




def student_login(request):
    stu_obj=models.Student.objects.filter(name='GDP',pwd='123456').first()
    print(stu_obj)
    request.session['student_info']={'id':stu_obj.nid,'user':stu_obj.name}
    return redirect('/answering/1/1/')
def answering(request,clsid, qsnreid):
    qr_obj=models.Questionnaire.objects.filter(cls__nid=clsid,nid=qsnreid).first()
    field_dict={}
    if qr_obj:
        questions_list=models.Questions.objects.filter(naire=qr_obj)
        for question in questions_list:
            if question.tp ==1:
                field_dict['val_%s' % question.id] = fields.ChoiceField(
                    label=question.title,
                    error_messages={'required':'请打分'},
                    widget=widgets.RadioSelect,
                    choices=[(i,i) for i in range(1,11)]
                )
            elif question.tp == 2:
                field_dict['option_id_%s'%question.id]=fields.ChoiceField(
                    label=question.title,
                    error_messages={'required':'请选择一个选项'},
                    widget=widgets.RadioSelect,
                    choices=models.Option.objects.filter(qs_id=question.id).values_list('id','title')
                )
            else:

                field_dict['context_%s'%question.id]=fields.CharField(
                    label=question.title,
                    help_text='长度不能超过十五个字',
                    widget=widgets.Textarea,validators=[func,]
                )
    answeringForm=type("answeringForm",(Form,),field_dict)

    if request.method == 'GET':
        form=answeringForm()
    elif request.method=='POST':
        print(request.POST)
        print(request.body)
        form=answeringForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            answer_list=[]
            for k,values in form.cleaned_data.items():
                key,ques_id=k.rsplit('_',1)
                anser_dict={'stu_nid':request.session['student_info']['id'],'question_id':ques_id,key:values}
                print(anser_dict)
                answer_list.append(models.Answer(**anser_dict))
            models.Answer.objects.bulk_create(answer_list)
            return HttpResponse('<h1>谢谢参与调查！</h1>')

    else:return HttpResponse('滚')
    return render(request,'answering.html',{'form':form})
