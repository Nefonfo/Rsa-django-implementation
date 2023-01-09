from django.contrib import admin
from .models import RsaKey


# Register your models here.
class RsaKeyAdmin(admin.ModelAdmin):
    readonly_fields = ('key_type', 'content')


admin.site.register(RsaKey, RsaKeyAdmin)
