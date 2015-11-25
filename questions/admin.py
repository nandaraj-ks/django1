from django.contrib import admin
from models import Question, QuestionLog

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
	pass
admin.site.register(Question, QuestionAdmin)

class QuestionLogAdmin(admin.ModelAdmin):
	pass
admin.site.register(QuestionLog, QuestionLogAdmin)