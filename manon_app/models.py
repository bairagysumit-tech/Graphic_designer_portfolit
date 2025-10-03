from django.db import models
from django.contrib.auth.models import User
#from django.utils.translation.trans_real import ACCEPT_LANGUAGE_HEADER_MAX_LENGTH
from django.conf.global_settings import AUTH_USER_MODEL
from autoslug.fields import AutoSlugField

# Create your models here.
class Design(models.Model):
    catagory = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='image', null=True, blank=True)
    ditels = models.TextField(null =True, blank = True)
    time = models.TimeField(auto_now=True, blank=True, null=True)
    image_slug = AutoSlugField(unique = True, null=True, populate_from = 'ditels', default = None)
    design_view = models.IntegerField(null=True, blank=True, default=0)
    design_like = models.IntegerField(null=True, blank=True, default=0)
    design_view1 = models.IntegerField(null=True, blank=True, default=0)
    design_like1 = models.IntegerField(null=True, blank=True, default=0)
    design_tag = models.TextField(null=True, blank=True)
    
class LikeDesign(models.Model):
    post = models.ForeignKey(to=Design, on_delete = models.CASCADE)
    user = models.ForeignKey(to=User, on_delete =models.CASCADE)
    like = models.BooleanField(default = False)
    cr_date = models.DateTimeField(auto_now = True)
    
        
class EmailStore(models.Model):
    email = models.EmailField()
    
class BlogData(models.Model):
    title1 = models.CharField(max_length=200 )
    blog =  models.TextField()
    time = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    like = models.IntegerField(null=True, blank = True, default=0)
    comment = models.IntegerField(null=True, blank = True, default=0)
    blog_view=models.IntegerField(null=True, blank = True, default=0)
    blog_tag = models.TextField(null=True, blank=True)
    blog_slug = AutoSlugField(unique = True, null=True, populate_from = 'title1', default = None )
    def __str__(self):
        return self.title1
    
    
class Image(models.Model):
    image_id = models.ForeignKey(BlogData, related_name="blog_image", on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'image', blank=True, null=True)
    img_alt = models.CharField(max_length = 50, blank = True, null = True)
    img_title = models.CharField(max_length = 50, blank = True, null = True)
    
    

class OtpStore(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    vrify  = models.BooleanField(default=False)
    cr_date = models.DateTimeField( auto_now = True)
    otp_count = models.IntegerField(blank = True, null = True, default=0)
    
class UserProfile(models.Model):
    user= models.OneToOneField(AUTH_USER_MODEL, related_name="user_profile", on_delete=models.CASCADE)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    p_image= models.ImageField(upload_to = 'image', blank=True, null=True)
    profile= models.CharField(max_length = 10, choices =(('user','user'), ('admin','admin'), ('staf','staf')), default="user")
    status = models.BooleanField(default=False)
    
    
class LikeData(models.Model):
    post = models.ForeignKey(to=BlogData, on_delete = models.CASCADE)
    user = models.ForeignKey(to=User, on_delete =models.CASCADE)
    like = models.BooleanField(default = False)
    cr_date = models.DateTimeField(auto_now = True)
    
class CommentData(models.Model):
    post = models.ForeignKey(to=BlogData, on_delete = models.CASCADE)
    user = models.ForeignKey(to=User, on_delete =models.CASCADE)
    comm = models.TextField()
    comm_status= models.CharField(max_length = 20, choices =(('Published','Published'), ('Under Review','Under Review')), default="Under Review", blank=True, null=True)
    cr_date = models.DateTimeField(auto_now = True)
    
class ReplyData(models.Model):
    post = models.ForeignKey(to=BlogData, on_delete = models.CASCADE)
    user = models.ForeignKey(to=User, on_delete =models.CASCADE)
    comment = models.ForeignKey(to=CommentData, on_delete =models.CASCADE)
    reply = models.TextField()
    cr_date = models.DateTimeField(auto_now = True)
    
    
class Subscribe(models.Model):
    email = models.EmailField()
    name  = models.CharField(max_length = 30, null=True, blank = True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    