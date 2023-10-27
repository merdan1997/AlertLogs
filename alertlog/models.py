from django.db import models



from django.contrib.auth.models import User

class Roles(models.Model):
    name = models.CharField(max_length=150 , null=False)
    description = models.TextField(null=False)
    severity_in = models.CharField(max_length=50, null= False)
    application = models.CharField(max_length = 100, null = False)
    index_number = models.CharField(max_length = 10 ,blank=True,  null=True)
    split_character = models.CharField(max_length =10, null=False)
    start_message = models.CharField(max_length = 10, default =None,blank =True , null=True)
    severity_out = models.CharField(max_length = 10, null =False)
    own_text = models.CharField(max_length = 150 , blank =True, null= True)
    # users = models.ManyToManyField(User)
    def __str__(self):
        return self.name


class Filterlog(models.Model):
    hostname = models.CharField(max_length=150, null=False)
    severity = models.CharField(max_length=50, null=False)
    facility = models.CharField(max_length=50, null=False)
    application = models.CharField(max_length=70, null=False)
    message  = models.TextField(null=False)
    timestamp =models.DateTimeField(auto_now=False)
    role = models.CharField(max_length=350, null=False)
    is_know = models.BooleanField(default =False)
    text_message = models.CharField(max_length=250, default=None, blank=True, null=True)
    # users = models.ManyToManyField(User)
    
    def __str__(self):
        return (self.hostname + self.message)
    
    
class Hostnames(models.Model):
    hostname  =  models.CharField(max_length=150, null=False)
    ipaddress = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.hostname

