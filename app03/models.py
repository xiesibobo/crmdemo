from django.db import models



# Create your models here.



class Boardroom(models.Model):
    rid = models.AutoField(primary_key=True)
    room_id = models.CharField(max_length=8)
    title = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    def __str__(self):
        return self.room_id + self.title

class Slot(models.Model):
    starttime = models.TimeField()
    endtime = models.TimeField()

    @property
    def title(self):
        return str(self.starttime)[:5] + '-' + str(self.endtime)[:5]


    def __str__(self):
        return str(self.starttime) +'-'+ str(self.endtime)

class Record(models.Model):
    boardroom = models.ForeignKey(to='Boardroom')
    slot = models.ForeignKey(to='Slot')
    user = models.ForeignKey(to='app01.UserInfo')
    day=models.DateField()
    create_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [
            ('boardroom', 'slot','day'),
        ]
    def __str__(self):
        return self.boardroom.title + str(self.slot.starttime)