from django.contrib import admin
from django.db import models  # Import models from django
from .models import Editorial, CryptoAnalysis, PressRelease, News, NewestCourse
from ckeditor.widgets import CKEditorWidget  # Import from ckeditor
from .models import Hashtag

class EditorialAdmin(admin.ModelAdmin):  # Use the regular ModelAdmin
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    list_display = ['title']
    autocomplete_fields = ['hashtags']

class PressReleaseAdmin(admin.ModelAdmin):  # Use the regular ModelAdmin
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    list_display = ['title']
    autocomplete_fields = ['hashtags']
    
# admin.py
class NewsAdmin(admin.ModelAdmin):  
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    list_display = ['title']
    autocomplete_fields = ['hashtags']
    list_display = ['title', 'pub_date', 'main_article_position']
    list_editable = ['main_article_position']
    list_filter = ['main_article_position']

# admin.py

class NewestCourseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    list_display = ['title']
    autocomplete_fields = ['hashtags']

class CryptoAnalysisAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    list_display = ['title', 'link']
    autocomplete_fields = ['hashtags']

class HashtagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(NewestCourse, NewestCourseAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Editorial, EditorialAdmin)
admin.site.register(CryptoAnalysis, CryptoAnalysisAdmin)
admin.site.register(PressRelease, PressReleaseAdmin)
