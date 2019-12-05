from django.contrib import admin
import taskmanager.models as db

# Register your models here.
admin.site.register(db.Role)
admin.site.register(db.User)
admin.site.register(db.Task)
admin.site.register(db.List)
admin.site.register(db.Note)