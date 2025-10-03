from django.contrib.sitemaps import Sitemap
from .models import Design
 
 
class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Design.objects.all()
    
    def location(self,obj):
        return '/blog/%s' % (obj.image_slug)