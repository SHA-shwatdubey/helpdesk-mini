from django.contrib import admin
from .models import Role, Ticket, Comment, Timeline

admin.site.register(Role)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Timeline)
