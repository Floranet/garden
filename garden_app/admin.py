from django.contrib import admin
# Register your models here.
from django.contrib.auth.hashers import make_password
from.models import user_reg,Feed_user,Feed_prof,prof_reg,pay,resource
from .models import*

admin.site.register(user_reg)
admin.site.register(Feed_user)
admin.site.register(prof_reg)
admin.site.register(Feed_prof)
admin.site.register(cart)
admin.site.register(pay)
admin.site.register(resource)
admin.site.register(shop)
admin.site.register(Reminder)
admin.site.register(Task)
admin.site.register(pTask)
admin.site.register(pReminder)

class UserRegAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'status']

    def save_model(self, request, obj, form, change):
        # Hash the password before saving if it's being set or changed
        if obj.password:
            obj.password = make_password(obj.password)  # Ensure password is hashed
        super().save_model(request, obj, form, change)