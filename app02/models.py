from django.db import models
from app01.models import UserInfo


# Create your models here.


#
# class Boardroom(models.Model):
#     rid = models.AutoField(primary_key=True)
#     room_id = models.CharField(max_length=8)
#     address = models.CharField(max_length=64)
#
#
# class Slot(models.Model):
#     starttime = models.DateTimeField()
#     endtime = models.DateTimeField()
#
#
# class Record(models.Model):
#     boardroom = models.ForeignKey(to='Boardroom')
#     slot = models.ForeignKey(to='Slot')
#     user = models.ForeignKey(to='UserInfo')
#
#     class Meta:
#         unique_together = [
#             ('boardroom', 'slot'),
#         ]
