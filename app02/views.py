from django.shortcuts import render,HttpResponse
from app02 import models
# Create your views here.
def subscrib(request):
    time_list=models.Slot.objects.all()
    room_list = models.Boardroom.objects.all()
    # def get_room():
    #     for room in room_list:
    #         def inner():
    #             for item in time_list:
    #                 record_obj = models.Record.objects.filter(slot=item, boardroom=room)
    #                 yield {'record_obj':record_obj,'time':item}
    #         yield inner()

    waper_list=[]
    for room in room_list:
        inner_list=[]
        for item in time_list:
            record_obj = models.Record.objects.filter(slot=item, boardroom=room)
            inner_list.append(record_obj)
        waper_list.append({'room':room,'inner_list':inner_list})


    # record_list=models.Record.objects.all()




    return render(request,'subscribemeeting.html',{'time_list':time_list,'waper_list':waper_list})



