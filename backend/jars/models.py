from django.db import models
from django.utils import timezone

class Jar(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    currency = models.CharField(max_length=3)
    added_at =  models.DateTimeField(default=timezone.now)


OPER_STAT = (
    ('success', 'success'),
    ('failed', 'failed')
)

OPER_TYPE = (
    ('add', 'add'),
    ('sub', 'sub')
)

class Operation(models.Model):
    title = models.CharField(max_length=50)
    jar = models.ForeignKey(Jar, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    currency = models.CharField(max_length=3)
    duration = models.CharField(max_length=10,blank=True)
    status = models.CharField(max_length=7, choices=OPER_STAT, default='success')
    type = models.CharField(max_length=3, choices=OPER_TYPE)