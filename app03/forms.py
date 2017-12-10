from django.forms import Form, fields, widgets
from app03 import models


class Appointment(Form):
    def __init__(self,*args,**kwargs):
        super(Appointment,self).__init__(*args,**kwargs)
        self.fields['slot'].choices =[(item.id,item.title)for item in models.Slot.objects.all()]

    day=fields.DateField(
        label='请选择预定日期',
        required=True,
        error_messages={'required': '请选择日期'},
        widget=widgets.SelectDateWidget()
    )
    room=fields.ChoiceField(
        widget=widgets.Select(attrs={}),
        choices=models.Boardroom.objects.all().values_list('rid','title')
    )
    slot=fields.ChoiceField(
        widget=widgets.Select(),
        # choices=models.Slot.objects.all().values_list('id','starttime')
    )