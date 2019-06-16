from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from task_app.models import Task, TaskTransaction
from django.contrib.auth import get_user_model
from authentication.models import User
from datetime import datetime
from authentication.decorators import is_delivery_person
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from store_manager_app import views

from delivery_person_app.serializers import FetchDeliveryTaskSerializer

@csrf_exempt
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@is_delivery_person
def list_tasks(request):
	try:
		tasks = FetchDeliveryTaskSerializer(Task.objects.filter(state=2, completed_by=request.user), many=True)
		return Response({'msg':'Tasks retrived successfully!', 'data':tasks.data},status = status.HTTP_200_OK)
	except Exception as e:
		return Response({'msg':str(e)}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@is_delivery_person
def decline_task(request):
	try:
		task_id = request.data.get('id')
		task = Task.objects.get(id=task_id, completed_by = request.user)
		if task.state == 2:
			task.state = 1
			task.completed_by = None
			task.save()
			task_transaction = TaskTransaction.objects.create(
				task = task,
				action = 4,
				performed_by = request.user
			)
			task_transaction.save()
			message = task.name+" "+" rejected by "+request.user.name
			notify_manager(task.created_by.id,message)
			views.send_high_prioirity_task()
			return Response({'msg':'Task declined successfully!'}, status=status.HTTP_200_OK)
		else:
			return Response({'msg':'cannot decline the task'}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({'msg':str(e)}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@is_delivery_person
def complete_task(request):
	try:
		task_id = request.data.get('id')
		task = Task.objects.get(id=task_id, completed_by = request.user)
		if task.state == 2:
			task.state = 3
			task.save()
			task_transaction = TaskTransaction.objects.create(
				task = task,
				action = 3,
				performed_by = request.user
			)
			task_transaction.save()
			return Response({'msg':'Task completed successfully!'}, status=status.HTTP_200_OK)
		else:
			return Response({'msg':'cannot complete the task'}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({'msg':str(e)}, status=status.HTTP_404_NOT_FOUND)

def notify_manager(room_id,message):
	channel_layer = get_channel_layer()
	room = 'manager_'+str(room_id)
	async_to_sync(channel_layer.group_send)(room, {
		"type": "chat.message",
		"room_id": room,
		"message": {"activity": 'accepted_task',"data":message},
	})


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@is_delivery_person
def accept_task(request):
	try:
		task_id = request.data.get('id')
		task_count = Task.objects.filter(state=2, completed_by=request.user).count()
		if task_count < 3:
			task = Task.objects.get(id=task_id)
			user = User.objects.get(email=request.user.email)
			if task.state == 1:
				Task.objects.filter(id=task_id).update(state=2,completed_by=request.user)
				task_transaction = TaskTransaction.objects.create(
					task = task,
					action = 2,
					performed_by = request.user
				)
				task_transaction.save()
				#sending notification alert
				message = task.name+" "+" task accepted by "+request.user.name
				notify_manager(task.created_by.id,message)
				views.send_high_prioirity_task()
				return Response({'msg':'Task accepted successfully!'}, status=status.HTTP_200_OK)
			else:
				return Response({'msg':'cannot accept the task'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'msg':'cannot accept the task due to pending tasks count'}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({'msg':str(e)}, status=status.HTTP_400_BAD_REQUEST)

def get_top_priority_task():
	tasks = FetchDeliveryTaskSerializer(Task.objects.filter(state=1).order_by('-priority','-created_on').first())
	return tasks

@csrf_exempt
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@is_delivery_person
def priority_task(request):
	try:
		tasks = get_top_priority_task()
		return Response({'msg':'Tasks retrived successfully!', 'data':tasks.data},status = status.HTTP_200_OK)
	except Exception as e:
		return Response({'msg':str(e)}, status=status.HTTP_404_NOT_FOUND)




