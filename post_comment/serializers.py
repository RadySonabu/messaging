from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import Message


class CreateMessageSerializer(serializers.ModelSerializer):
    # replies = RecursiveField(many=True,allow_null=True,required=False)
    userId = serializers.CharField(source='name',allow_blank=True,allow_null=True)
    # id = serializers.PrimaryKeyRelatedField(source='collaborate_messaging_a00_rec',queryset=Message.objects.all())
    # threadId = serializers.CharField(source='parent',allow_blank=True,allow_null=True,required=False)
    message = serializers.CharField(source='message_content')
    # contactId = serializers.CharField(source='contact_id')
    groupId = serializers.CharField(source='group_id')
    # dateCreated = serializers.CharField(source='date_created',allow_blank=True,allow_null=True)
    # displayPhotoSrc = serializers.CharField(source='photo',allow_blank=True,allow_null=True,required=False)
    
    class Meta:
        model = Message
        fields = ['threadId','groupId','userId','message',]

    def create(self, validated_data):

        message = Message.objects.create(
            threadId=validated_data.get('threadId', None),
            group_id=validated_data['group_id'],
            name=validated_data['name'],
            message_content=validated_data['message_content'],
            
            
        )
        return message


class MessageSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True,allow_null=True,required=False)
    userId = serializers.CharField(source='name',allow_blank=True,allow_null=True)
    # id = serializers.PrimaryKeyRelatedField(source='collaborate_messaging_a00_rec',queryset=Message.objects.all())
    # threadId = serializers.CharField(source='parent',allow_blank=True,allow_null=True,required=False)
    message = serializers.CharField(source='message_content')
    # contactId = serializers.CharField(source='contact_id')
    groupId = serializers.CharField(source='group_id')
    dateCreated = serializers.CharField(source='date_created',allow_blank=True,allow_null=True)
    displayPhotoSrc = serializers.CharField(source='photo',allow_blank=True,allow_null=True,required=False)
    
    class Meta:
        model = Message
        fields = [  
                    'id',
                    # 'threadId',
                    'groupId',
                    'userId',
                    'message',
                   
                    'dateCreated',
                    'displayPhotoSrc',
                    'replies',
                    ]
        # extra_kwargs = {
        #     'url': {'lookup_field': 'groupId'}
        # }

    # def create(self, validated_data):
        
    #     message = Message.objects.create(
    #         parent=validated_data.get('threadId', None),
    #         group_id=validated_data['group_id'],
            
    #         message_content=validated_data['message_content'],
    #         date_created=validated_data['date_created'],
    #         photo=validated_data.get('photo', None),
    #     )
    #     return message



        
    