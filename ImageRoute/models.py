from django.db import models
from django.contrib.auth.models import User

class BackgroundImage(models.Model):
    name = models.CharField(max_length=200)
    #some variable related to the image
    image = models.ImageField(upload_to='backgrounds/', null=True, blank=True)
    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    background = models.ForeignKey(BackgroundImage, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name

class RoutePoint(models.Model):
    route = models.ForeignKey(Route, related_name="points", on_delete=models.CASCADE)
    order = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        ordering = ['order']

# Board game

class GameBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    cols = models.PositiveIntegerField()
    dots = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.title} ({self.rows}×{self.cols})"

class Path(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(GameBoard, on_delete=models.CASCADE)
    lines = models.JSONField(default=list, blank=True) # { row1 , row2, col1, col2, color}

    class Meta:
        unique_together = ('user', 'board')  #