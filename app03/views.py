import datetime,json
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse

from app03 import models,forms

# Create your views here.
def subscrib(request):
    user_id=request.user.id
    if not user_id:
        return HttpResponse('滚')
    if request.method=='POST':
        appointment_days = '{0}-{1}-{2}'.format(*[request.POST.get(i) for i in ['day_year','day_month','day_day']])
        slot=request.POST.get('slot')
        room=request.POST.get('room')
        obj=models.Record.objects.create(day=appointment_days,boardroom_id=room,slot_id=slot,user_id=user_id)
        if obj:
            return HttpResponse('预约成功')
        else:
            return HttpResponse('该时间段内房间已被预订，请核实')
    time_list=models.Slot.objects.all()
    room_list = models.Boardroom.objects.all()
    appointment_day=request.GET.get('appointment_day')
    form = forms.Appointment()
    #如果没有指定哪天，默认当天
    if not appointment_day:
        appointment_day = datetime.datetime.now().strftime('%Y-%m-%d')

    waper_list=[]
    for room in room_list:
        inner_list=[]
        for item in time_list:
            record_obj = models.Record.objects.filter(slot=item, boardroom=room,day=appointment_day)
            inner_list.append(record_obj)
        waper_list.append({'room':room,'inner_list':inner_list})


    # record_list=models.Record.objects.all()

    # appointment_day='{0}年{1}月{2}日'.format(*appointment_day.split('-'))


    return render(request,'subscribemeeting.html',{'form':form,'time_list':time_list,'waper_list':waper_list,'appointment_day':appointment_day})


def fotest(request):
    form=forms.Appointment()
    return render(request,'test.html',{'form':form})



def subscrib2(request):
    user_id=request.user.id
    if not user_id:
        return HttpResponse('滚')
    if request.is_ajax():
        ret={'addflag':False,'addmsg':None,'delflag':False,'delmsg':None}
        dic=json.loads(request.POST.get('data'))
        # appointment_days = '{0}-{1}-{2}'.format(*[request.POST.get(i) for i in ['day_year','day_month','day_day']])
        print('dic',dic['add'])
        print('dic',type(dic['add']))
        create_list=[]
        for add_x,additem_item in dic['add'].items():
            print(add_x,additem_item)
            # additem_item=json.loads(additem_item)

            appointment_days=additem_item.get('date')
            slot=additem_item.get('slot')
            room=additem_item.get('room_id')
            obj=models.Record(day=appointment_days,boardroom_id=room,slot_id=slot,user_id=user_id)
            create_list.append(obj)
        add_flag=models.Record.objects.bulk_create(create_list)
            # obj=models.Record.objects.create(day=appointment_days,boardroom_id=room,slot_id=slot,user_id=user_id)
        del_flag=models.Record.objects.filter(id__in=dic['del']).delete()
        if add_flag:
            ret['addflag']=True
            ret['addmsg']='预约成功'
        else:
            ret['addmsg'] ='该时间段内房间已被预或未选择'

        if del_flag:
            ret['delflag'] = True
            ret['delmsg'] = '取消成功'
        else:
            ret['delmsg'] = '取消失败'
        return JsonResponse(ret)
    time_list=models.Slot.objects.all()
    form = forms.Appointment()


    # record_list=models.Record.objects.all()

    # appointment_day='{0}年{1}月{2}日'.format(*appointment_day.split('-'))


    return render(request,'subscribemeeting2.html',{'form':form,'time_list':time_list})


def getmeeting(request):

    room_list = models.Boardroom.objects.all().values('rid','title')
    print(request.GET)
    appointment_day = request.GET.get('appointment_day')
    time_list = models.Slot.objects.all()

    # 如果没有指定哪天，默认当天
    if not appointment_day:
        appointment_day = datetime.datetime.now().strftime('%Y-%m-%d')

    waper_list = []
    for room in room_list:
        inner_list = []
        for item in time_list:
            record_obj = models.Record.objects.filter(slot=item, boardroom=room['rid'], day=appointment_day).values('id','user__username')
            if record_obj:
                record_obj=record_obj[0]
                record_obj['class']='active'
                record_obj['user_id']=request.user.id
            else:record_obj={}
            record_obj['slot']= item.id
            inner_list.append(record_obj)
        waper_list.append({'title': room['title'], 'room_id':room['rid'],'inner_list': inner_list})
    ret = {'waper_list': waper_list}
    print(type(ret['waper_list']))
    # return HttpResponse(waper_list)
    return JsonResponse(ret)