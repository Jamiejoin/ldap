from django.contrib import admin
from models import *

class ManageAdmin(admin.ModelAdmin):
    search_fields = ('name', 'remark')
    radio_fields = {"ops_manage": admin.VERTICAL}

admin.site.register(manage, ManageAdmin)