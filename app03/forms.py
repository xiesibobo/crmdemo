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
        widget=widgets.SelectDateWidget(attrs={'class':'form-inline'})
    )
    room=fields.ChoiceField(
        label='请选择房间',
        widget=widgets.Select(attrs={'class':'form-control'}),
        choices=models.Boardroom.objects.all().values_list('rid','title')
    )
    slot=fields.ChoiceField(
        label='请选择时间段',
        widget=widgets.Select(attrs={'class':'form-control'}),
        # choices=models.Slot.objects.all().values_list('id','starttime')
    )