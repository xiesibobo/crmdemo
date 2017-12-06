from django.forms import ModelForm
from app01 import models

class QuestionsModelForm(ModelForm):
    class Meta:
        model=models.Questions
        fields=['title','tp']
        labels={
            'title':'标题：',
            'tp':'类型：'
        }


class OptionModelForm(ModelForm):
    class Meta:
        model=models.Option
        fields=['title','score']