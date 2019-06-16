from django.db import models
from authentication.models import User


class Task(models.Model):

	LOW = 1
	MEDIUM = 2
	HIGH = 3
	
	__task_priority_choices = (
        (LOW,'Low Priority'),
        (MEDIUM,'Medium Priorityy'),
        (HIGH,'High Priority')
    )

	NEW = 1
	ACCEPTED = 2
	COMPLETED = 3
	DECLINED = 4
	CANCELED = 5

	__task_state_choices = (
		(NEW,'New'),
		(ACCEPTED,'Accepted'),
		(COMPLETED,'Completed'),
		(DECLINED,'Declined'),
		(CANCELED,'Canceled')
	)

	name = models.CharField(max_length = 80)
	priority = models.SmallIntegerField(choices=__task_priority_choices, default=LOW)
	state = models.SmallIntegerField(choices=__task_state_choices, default=NEW)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_by')
	created_on = models.DateTimeField(auto_now_add=True)
	completed_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='completed_by',blank=True,null=True)
	completed_on = models.DateTimeField(auto_now=True,blank=True,null=True)

class TaskTransaction(models.Model):

	NEW = 1
	ACCEPTED = 2
	COMPLETED = 3
	DECLINED = 4
	CANCELED = 5

	__task_action_choices = (
    	(NEW,'New'),
    	(ACCEPTED,'Accepted'),
    	(COMPLETED,'Completed'),
    	(DECLINED,'Declined'),
    	(CANCELED,'Canceled')
    )

	task = models.ForeignKey(Task,on_delete=models.CASCADE)
	action = models.SmallIntegerField(choices=__task_action_choices, default=NEW)
	performed_by = models.ForeignKey(User,on_delete=models.CASCADE)
	performed_on = models.DateTimeField(auto_now_add=True)
