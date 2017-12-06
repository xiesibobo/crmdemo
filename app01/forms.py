from django.forms import Form, fields, widgets,ModelForm
from django.core.validators import ValidationError,RegexValidator
from app01 import models


class QuestionnaireForm(Form):
    def __init__(self,request,*args,**kwargs):
        super(QuestionnaireForm,self).__init__(*args,**kwargs)
        self.fields['cls'].choices =models.ClassList.objects.all().values_list('nid','name')
        self.fields['creator'].choices=models.UserInfo.objects.values_list('id','username')
    title = fields.CharField(
        max_length=64,
        required=True,
        error_messages={'required': '标题不能为空'},
        widget=widgets.TextInput(attrs={'placeholder': '标题','class': 'form-control'})
    )
    cls = fields.ChoiceField(
        label='班级：',
        widget=widgets.Select(attrs={ 'class': 'list-inline'})
    )
    creator = fields.ChoiceField(
        label='创建者：',
        widget=widgets.Select(attrs={ 'class': 'list-inline'})
    )



class QuestionsForm(Form):
    def __index__(self,*args, **kwargs):
        super(QuestionsForm, self).__init__(*args, **kwargs)

        self.fields['tp'].initial=[1]
    title=fields.CharField(
        label='标题：',
        max_length=64,
        required=True,
        error_messages={'required': '标题不能为空'},
        widget=widgets.TextInput(attrs={'placeholder': '标题', 'class': 'form-inline'})
    )
    tp=fields.IntegerField(
        label='题目类型：',
        widget=widgets.Select(attrs={'class': 'form-inline types'},choices=((1,'打分'),(2,'单选'),(3,'评价')))
    )

class OptionForm(Form):
    title=fields.CharField(
        label='标题：',
        max_length=64,
        required=True,
        error_messages={'required': '标题不能为空'},
        widget=widgets.TextInput(attrs={'placeholder': '标题', 'class': 'form-inline'})
    )
    score=fields.IntegerField(
        label='分值：',
        required=True,
        widget=widgets.NumberInput()
    )


