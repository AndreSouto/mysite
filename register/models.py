from django.db import models

# Create your models here.
class User(models.Model):

    def User(self,name,password):
        self.name = name
        self.password = password

    def setName(self,n):
        self.name = n

    def getName(self):
        return self.name

    def setPassword(self,p):
        self.password = p

    def getPassword(self):
        return self.password
