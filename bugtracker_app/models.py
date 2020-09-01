from django.db import models
from django.utils import timezone
from customuser_app.models import CustomUser

#Howard Post assisted me in writing this code.


class Tickets(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW'
        IN_PROGRESS = 'IN PROGRESS'
        DONE = 'DONE'
        INVALID = 'INVALID'
    title = models.CharField(max_length=80)
    created = models.DateField(default=timezone.now)
    description = models.TextField()
    filed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='user_assigned', blank=True, null=True)
    completed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='user_completed', blank=True, null=True)


    @property
    def ticket_age(self):
        start_date = timezone.datetime.strptime(str(self.created), '%Y-%m-%d')
        str_time = str(timezone.now())
        timelength = len(str_time)-6
        str_time = str_time[:timelength]
        endtime = timezone.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S.%f')
        return abs((endtime-start_date).days)

