from django.db import models

# Create your models here.
class Message(models.Model):
    id = models.AutoField(primary_key=True,db_column='collaborate_messaging_a00_rec')
    threadId = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, db_column='parent_post_id')
    message_content = models.TextField()
    name = models.CharField(max_length=50)
    
    group_id = models.CharField( max_length=50)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    photo  = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return f'{self.id}'
    
    # class Meta:
        # order_with_respect_to = 'threadId'