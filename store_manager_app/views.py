from django.shortcuts import render
from store_manager_app.serializers import TaskSerializer, FetchTaskSerializer, FetchTaskTransactionsSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from task_app.models import Task, TaskTransaction
from django.contrib.auth import get_user_model
from authentication.models import User
from datetime import datetime
from authentication.decorators import is_store_manager
from delivery_person_app.views import get_top_priority_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_high_prioirity_task():
	channel_layer = get_channel_layer()
	task = get_top_priority_task()
	async_to_sync(channel_layer.group_send)("delivery_person", {
		"type": "chat.message",
		"room_id": 'delivery_person',
		"message": {"activity": 'priority_task',"data":task.data},
	})

@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@is_store_manager
def create_task(request):
	task_serializer = TaskSerializer(data=request.data)
	if task_serializer.is_valid():
		task_obj = Task.objects.create(
			name=request.data.get('name'),
			priority=request.data.get('priority'),
			created_by=request.user,
			created_on=datetime.now()
		)
		task_obj.save()
		task_transaction_obj = TaskTransaction.objects.create(
			task = task_obj,
			action = 1,
			performed_by = request.user
		)
		task_transaction_obj.save()
		send_high_prioirity_task()
		
		return Response(task_serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(task_serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@is_store_manager
def cancel_task(request):
	task_id = request.data.get('id')
	try:
		task = Task.objects.get(id=task_id)
		if task.state == 1:
			task.state = 5
			task.save()
			task_transaction_obj = TaskTransaction.objects.create(
				task = task,
				action = 5,
				performed_by = request.user
			)
			task_transaction_obj.save()
			send_high_prioirity_task()
			return Response({'msg':'Task cancelled successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'msg':'cannot cancel the task'}, status=status.HTTP_400_BAD_REQUEST)
	except:
		return Response({'msg':'Task not found'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@is_store_manager
def list_tasks(request):
	try:
		tasks = FetchTaskSerializer(Task.objects.filter(created_by = request.user), many=True)
		return Response({'msg':'Tasks retrived successfully!', 'data':tasks.data},status = status.HTTP_200_OK)
	except Exception as e:
		return Response({'msg':str(e)}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@is_store_manager
def list_task_transactions(request):
	try:
		task = Task.objects.get(id=request.data.get('id'))
		task_transactions =  FetchTaskTransactionsSerializer(TaskTransaction.objects.filter(task = task), many=True)
		return Response({'msg':'Task transactions retrived successfully!', 'data':task_transactions.data},status = status.HTTP_200_OK)
	except Exception as e:
		return Response({'msg':str(e)}, status=status.HTTP_404_NOT_FOUND)