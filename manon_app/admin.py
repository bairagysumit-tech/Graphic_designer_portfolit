from django.contrib import admin
from manon_app import models

# Register your models here.
class DesignAdmin(admin.ModelAdmin):
    list_display = ['id','catagory', 'image', 'ditels', 'design_view']
admin.site.register(models.Design, DesignAdmin)

class EmailFild(admin.ModelAdmin):
    list_dsiplay = ['id','email']
admin.site.register(models.EmailStore, EmailFild)

class BlogList(admin.ModelAdmin):
    list_dsiplay = ['id','title1' ]
admin.site.register(models.BlogData, BlogList)


class ImageList(admin.ModelAdmin):
    list_display = ['id', 'image_id', 'image']
    
admin.site.register(models.Image, ImageList)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'f_name','l_name', 'profile', 'p_image','status']
    list_editable= ['profile','status']
admin.site.register(models.UserProfile, UserProfileAdmin)

class UserSubs(admin.ModelAdmin):
    list_display = ['id', 'name','email']
admin.site.register(models.Subscribe, UserSubs)


