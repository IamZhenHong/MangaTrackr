from django.db import models

# Create your models here.

# class Page(models.Model):
#     url = models.CharField(max_length=200, null=True, blank=True)
#     pagelist = models.ForeignKey('PageList', on_delete=models.CASCADE, null=True, blank=True)


#     def __str__(self):
#         return self.url
    
class Link(models.Model):
    # page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Untitled Link (ID: {})".format(self.id)
        
# class PageList(models.Model):
#     url = models.CharField(max_length=200, null=True, blank=True)
#     title = models.CharField(max_length=200, null=True, blank=True)

#     def __str__(self):
#         return self.title
