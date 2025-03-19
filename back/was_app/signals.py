from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Messages

@receiver(post_save, sender=Messages)
def message_created(sender, instance, created, **kwargs):
    if created:
        print(f"\n=== Trying to send message {instance.id} ===")
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'wall_updates',
                {
                    'type': 'new_message',
                    'message': {
                        'id': instance.id,
                        'topic': instance.topic,
                        'text': instance.text,
                        'author': instance.author.id if instance.author else None,
                        'timestamp': instance.timestamp.isoformat(),
                    }
                }
            )
            print("=== Message sent successfully ===")
        except Exception as e:
            print(f"!!! Error sending message: {str(e)} !!!")