from django.contrib import admin

from .models import Question,Choice,Pirvate_Choice,Pirvate_Question

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Pirvate_Question)
admin.site.register(Pirvate_Choice)