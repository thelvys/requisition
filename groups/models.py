from django.db import models

from config import settings


class Department(models.Model):
    dep_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    main_dep = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    supervisor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="departments")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.dep_name
    

class Category(models.Model):
    cat_name = models.CharField(max_length=255, unique=True)
    main_cat = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.cat_name