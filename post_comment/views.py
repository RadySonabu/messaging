from django.http import JsonResponse
from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializer, CreateMessageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics, viewsets, views
from collections import OrderedDict
import requests
import json
from rest_framework import filters
from django.core.paginator import Paginator

class CreateMessageView(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = CreateMessageSerializer
    lookup_field = 'group_id'
    http_method_names = ['post', 'put']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        id = request.user.id
        token = request.META['HTTP_AUTHORIZATION']
        headers = {"Authorization" : f'{token}'}
        r = requests.get(f'https://abstract-user-dot-heroic-climber-277222.df.r.appspot.com/user/list/{id}', headers=headers)

        data = r.json()#['results']
        first_name = data['firstName']
        last_name = data['lastName']
        
        
        serializer.validated_data['userId'] = f'{first_name} {last_name}'
        
        
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)

        data = serializer.data
        
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class MessageView(ModelViewSet):
    queryset = Message.objects.filter(threadId__isnull=True)
    serializer_class = MessageSerializer
    lookup_field = 'group_id'
    http_method_names = ['get','list', 'delete', 'put']
    filterset_fields = ['name',]
    
    
    def list(self, request, *args, **kwargs):
        
        try:
            
            queryset_first = Message.objects.all().filter(threadId__isnull=True).order_by('-replies').distinct()
            queryset = queryset_first
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data_origin = serializer.data
                data = []
                id = request.user.id
                token = request.META['HTTP_AUTHORIZATION']
                headers = {"Authorization" : f'{token}'}

                r = requests.get(f'https://abstract-user-dot-heroic-climber-277222.df.r.appspot.com/user/list/{id}', headers=headers)

                user = r.json()#['results']
                replies = []
                for d in data_origin:
                    replies.append({
                        "id": d['id'],
                        # "parent": d['parent'],
                        "groupId" : d['groupId'],
                        "user":  user,
                        "message": d['message'],
                        "dateCreated": d['dateCreated'],
                        # "replies": d['replies'],
                    })
                # print(replies)
                for d in data_origin:
                    
                    data.append({
                        "id": d['id'],
                        # "parent": d['parent'],
                        "groupId" : d['groupId'],
                        "user":  user,
                        "message": d['message'],
                        "dateCreated": d['dateCreated'],
                        # "replies": d['replies'],
                        # "displayPhotoSrc": d['displayPhotoSrc'],

                    })


                return self.get_paginated_response(data)

            serializer = self.get_serializer(queryset, many=True)

            data_origin = serializer.data
            data = []
            for d in data_origin:
                
                data.append({
                    "id": d['id'],
                    # "parent": d['parent'],
                    "groupId" : d['groupId'],
                    "name": d['name'],
                    "message": d['message'],
                    "dateCreated": d['dateCreated'],
                    "displayPhotoSrc": 'Hello.png',
                    "replies": d['replies']
                })
            return Response(data)
        except Exception:
            return Response('No Bearer Token passed')

    def retrieve(self, request, *args, **kwargs):
        values = []
        # instance = self.get_object()
        instance = self.kwargs['group_id']
        
        parent = Message.objects.all().filter(threadId=None,group_id=instance)
        
        for parent in parent:
            values.append(parent.id)
        # children = Message.objects.all().filter(threadId__in=values)
        # children_values = children.values_list('id', flat=True)
        # for child in children_values:
        #     values.append(child)
        
        queryset = Message.objects.filter(id__in=values).order_by('-date_created')
        
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data_origin = serializer.data
            data = []
            id = request.user.id
            token = request.META['HTTP_AUTHORIZATION']
            headers = {"Authorization" : f'{token}'}

            for d in data_origin:
                child = []
                replies = []
                id = d['userId']
                
                r = requests.get(f'https://abstract-user-dot-heroic-climber-277222.df.r.appspot.com/user/list/{id}', headers=headers)
                
                user = r.json()
                children = Message.objects.all().filter(threadId=d['id'])
                for data_children in children:
                    child.append(data_children)
                for data_child in child:
                    replies.append({
                    "id": data_child.id,
                    "groupId" : data_child.group_id,
                    "user":  user,
                    "message": data_child.message_content,
                    "dateCreated": data_child.date_created,
                    })
                data.append({
                    "id": d['id'],
                    "groupId" : d['groupId'],
                    "user":  user,
                    "message": d['message'],
                    "dateCreated": d['dateCreated'],
                    "replies": replies,
                    

                })


            return self.get_paginated_response(data)






@api_view(['GET', 'POST'])
def show_group_member(request, pk):

    detail_list = []
    user_list = []
    list = []
    groups = []
    token = request.META['HTTP_AUTHORIZATION']
   
    headers = {"Authorization" : f'{token}'}
    contact_id = request.user.id
    print(contact_id)
    group_detail = requests.get(f'https://contact-dot-heroic-climber-277222.df.r.appspot.com/api/group-detail/?contact_id={contact_id}', headers=headers)
    print(group_detail)
    print(group_detail.json())
    data_origin = group_detail.json()['results']

    
    for d in data_origin:
        groups.append(d['group_id'])

    for g in groups:
        group_detail = requests.get(f'https://contact-dot-heroic-climber-277222.df.r.appspot.com/api/group-detail/?group_id={g}', headers=headers)
    
        gd = group_detail.json()['results']
    
    for g in gd:
        user_list.append(g['contact_id'])

    for u in user_list:
        user = requests.get(f'https://abstract-user-dot-heroic-climber-277222.df.r.appspot.com/user/list/{u}', headers=headers)
        data = user.json()
        list.append(data)
    x = 0  
    for g in gd:
        detail_list.append({
            "id": g['group_a01_rec'],
            "userId": g['contact_id'],
            "user": list[x],
            "isActive": g['active_status'],
            "role": g['group_role']
        })
        x = x+1
    group_list = []
    paginator = Paginator(detail_list, 10)
    for g in groups:
        group = requests.get(f'https://contact-dot-heroic-climber-277222.df.r.appspot.com/api/group/{g}', headers=headers)
        
        grp = group.json()
        
        group_list.append({
            "id": grp['id'],
            "name": grp['name'],
            "email": grp['email'],
            "members": detail_list,
            "type": grp['agent'],
            "dateUpdated": grp['dateUpdated'],
            "dateCreated": grp['dateCreated']
            
        })

    return JsonResponse(group_list,safe=False)

class GroupMember(generics.ListAPIView):

    
    def get(request):

        detail_list = []
        user_list = []
        list = []
        groups = []
        token = request.META['HTTP_AUTHORIZATION']
    
        headers = {"Authorization" : f'{token}'}
        contact_id = request.user.id
        group_detail = requests.get(f'https://contact-dot-heroic-climber-277222.df.r.appspot.com/api/group-detail/?contact_id={contact_id}', headers=headers)
    
        
        data_origin = group_detail.json()['results']

        
        for d in data_origin:
            groups.append(d['group_id'])

        for g in groups:
            group_detail = requests.get(f'https://contact-dot-heroic-climber-277222.df.r.appspot.com/api/group-detail/?group_id={g}', headers=headers)
        
            gd = group_detail.json()['results']
        
        for g in gd:
            user_list.append(g['contact_id'])

        for u in user_list:
            user = requests.get(f'https://abstract-user-dot-heroic-climber-277222.df.r.appspot.com/user/list/{u}', headers=headers)
            data = user.json()
            list.append(data)
        x = 0  
        for g in gd:
            detail_list.append({
                "id": g['group_a01_rec'],
                "userId": g['contact_id'],
                "user": list[x],
                "isActive": g['active_status'],
                "role": g['group_role']
            })
            x = x+1
        group_list = []
        paginator = Paginator(detail_list, 10)
        for g in groups:
            group = requests.get(f'https://contact-dot-heroic-climber-277222.df.r.appspot.com/api/group/{g}', headers=headers)
            
            grp = group.json()
            
            group_list.append({
                "id": grp['id'],
                "name": grp['name'],
                "email": grp['email'],
                "members": detail_list,
                "type": grp['agent'],
                "dateUpdated": grp['dateUpdated'],
                "dateCreated": grp['dateCreated']
                
            })

        return JsonResponse(group_list,safe=False)



@api_view(['GET','POST'])
def get_comment_count(request, pk):
    try:
        parent = Message.objects.all().filter(threadId=None,group_id=pk)
        children = Message.objects.all().filter(threadId=parent[0].id)
        children_count = children.values_list('id', flat=True).count()

        return Response(children_count)
    except Exception:
        return Response("Pass a valid group id!")
        

@api_view(['GET',])
def get_thread(request,pk):
    token = request.META['HTTP_AUTHORIZATION']
    headers = {"Authorization" : f'{token}'}
    data = []
    response = []
    children = Message.objects.filter(threadId=pk).order_by('-date_created')
    
    for d in children:
        data.append(d
            
        )
    
    for d in data:
        id = d.name
                
        r = requests.get(f'https://abstract-user-dot-heroic-climber-277222.df.r.appspot.com/user/list/{id}', headers=headers)

        user = r.json()#['results']
        response.append({
            "id": d.id,
            "groupId" : d.group_id,
            "user":  user,
            "message": d.message_content,
            "dateCreated": d.date_created,
        })
    
    return Response(response)