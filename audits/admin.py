from django.contrib import admin
from .models import Audit, RawRow, Activity

admin.site.register(Audit)
admin.site.register(RawRow)
admin.site.register(Activity)