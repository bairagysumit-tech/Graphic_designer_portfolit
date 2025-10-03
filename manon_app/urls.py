
from django.contrib import admin
from django.urls import path
from manon_app import views
from django.template.defaulttags import url
from .sitemaps import ArticleSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from manon import settings

app_name = "main"

sitemaps = {
    'blog':ArticleSitemap
}

urlpatterns = [
    
    path('', views.Home),
    path('about/', views.About),
    path('portfolio/', views.Portfolio),
    path('blog/', views.Blog),
    path('contact/', views.Contact),
    path('blog_view/', views.blogview),
    path('signin/', views.SignIn),
    path('signup/', views.SignUp),
    path('emailsend/', views.testemail),
    path('sigp/', views.signup_test),
    path('otp_check/', views.OtpCheck),
    path('design_upload/', views.design_upload),
    path('blog_insert/', views.BlogInsert),
    path('signout/', views.SignOut),
    path('blog_delete/<int:pk>/', views.Blog_Delete),
    path('blog_edit/<int:pk>/', views.Blog_Edit),
    path('blog_ditels/<blog_slug>/', views.BlogDitels),
    path('postlike/', views.PostLike),
    path('blog_public_privet/', views.BlogPP),
    path('comment-reply/', views.CommentReply),
    path('design-insert/', views.DesignInsert),
    path('design-update/<int:pk>/', views.DesignUpdate),
    path('design-delete/<int:pk>/', views.DesignDelete),
    path('design-ditels/<image_slug>/', views.DesignDitels),
    path('all-design/<designtype>/', views.AllDesign),
    path('all-signin/', views.AllSignin),
    path('email_subscribe/', views.EmailSubs),
    path('design_view_count/', views.DesignViewCount),
    path('design_like/', views.DesignLike),
    path('blog_view_count/', views.BlogViewCount),
    path('blog-image-delete/', views.BlogImageDelete),
    path('comment-status/', views.CommentStatus),
    path('comment-delete/', views.CommentDelete),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
