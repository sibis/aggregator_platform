from rest_framework import serializers
from task_app.models import Task, TaskTransaction
from authentication.models import User
from django.contrib.auth import get_user_model
from datetime import datetime

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','name','email')


class  FetchDeliveryTaskSerializer(serializers.ModelSerializer):
	created_by = UsersSerializer(required=True, allow_null=False)
	completed_by = UsersSerializer(required=True, allow_null=False)

	class Meta:
		model = Task
		fields = ('id','name','priority','state','created_by','created_on','completed_by','completed_on')
		related_object = 'created_by','completed_by'