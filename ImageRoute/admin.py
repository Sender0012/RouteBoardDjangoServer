from django.contrib import admin
from .models import User, Route, BackgroundImage, GameBoard

# admin.site.register(User)
admin.site.register(BackgroundImage)

@admin.register(GameBoard)
class GameBoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'rows', 'cols']
    # inlines = [DotInline]
# Register your models here.
