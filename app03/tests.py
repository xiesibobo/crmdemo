from django.test import TestCase

# Create your tests here.
appointment_day='{0}年{1}月{2}日'.format(*'2017-12-12'.split('-'))
print(appointment_day)