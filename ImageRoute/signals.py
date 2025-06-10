# your_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GameBoard, Path
from .sse import broadcast

@receiver(post_save, sender=GameBoard)
def board_created(sender, instance, created, **kwargs):
    if created:
        data = {
            "board_id": instance.id,
            "board_name": instance.title,
            "creator_username": instance.user.username
        }
        broadcast(event="newBoard", data=data)

@receiver(post_save, sender=Path)
def path_created(sender, instance, created, **kwargs):
    data = {
        "path_id": instance.id,
        "board_id": instance.board.id,
        "board_name": instance.board.title,
        "user_username": instance.user.username
    }
    broadcast(event="newPath", data=data)
