from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
class UserInfo(AbstractUser):
    def __str__(self):
        return self.username





class ClassList(models.Model):
    '''
    班级列表
    '''
    nid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=24)
    def __str__(self):
        return self.name

class Student(models.Model):
    '''
    学生表
    '''
    nid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=16)
    cls=models.ForeignKey(to='ClassList')
    def __str__(self):
        return self.name

class Questionnaire(models.Model):
    '''
    问卷表
    '''
    nid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=64)
    cls=models.ForeignKey(to='ClassList')
    creator=models.ForeignKey(to='UserInfo')
    def __str__(self):
        return self.title
    def Mate(self):
        return self.title

class Questions(models.Model):

    title=models.CharField(max_length=64)
    question_types=(
        (1,'打分'),
        (2,'单选'),
        (3,'评价')
    )
    tp=models.IntegerField(choices=question_types)
    def __str__(self):
        return self.title


class Option(models.Model):
    title=models.CharField(verbose_name='选项名称',max_length=32)
    score=models.IntegerField(verbose_name='选项对应的分值')
    qs=models.ForeignKey(to=Questions)
    def __str__(self):
        return self.title


class Answer(models.Model):
    stu=models.ForeignKey(to='Student')
    question=models.ForeignKey(to='Questions')
    option=models.ForeignKey(to='Option',null=True,blank=True)
    val=models.IntegerField(null=True,blank=True)
    content=models.CharField(max_length=255,null=True,blank=True)

