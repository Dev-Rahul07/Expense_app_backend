from django.db import models

class UserDetail(models.Model):
    FullName = models.CharField(max_length=100)
    Email = models.EmailField(unique=True) #ensure email is unique
    Password = models.CharField(max_length=100)
    RedDate = models.DateTimeField(auto_now_add=True) #used to store the date and time when the record was created
    
    
class Expense(models.Model):
    UserID = models.ForeignKey(UserDetail,on_delete=models.CASCADE) #if user is not exist then delete all the expenses of that User
    ExpenseDate = models.DateField(null=True,blank=True) 
    ExpenseItem = models.CharField(max_length=100) 
    ExpenseCost = models.CharField(max_length=100)
    NoteDate = models.DateTimeField(auto_now_add=True) #used to store the date and time when the record was created