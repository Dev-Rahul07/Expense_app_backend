from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse  # for sending json response
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *

#Signup API
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        FullName = data.get('FullName')
        Email = data.get('Email')
        Password = data.get('Password')
        
        
        
        if UserDetail.objects.filter(Email = Email).exists():
            return JsonResponse({'message':'Email already exists'},status = 400)
        UserDetail.objects.create(FullName = FullName,Email = Email,Password = Password)
        return JsonResponse({'message':'User is Registered Successfully '},status = 201)

# login API
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body) #convert json into python data 
        print(data)
        Email = data.get('Email')
        Password = data.get('Password')
        
        try:
            user = UserDetail.objects.get(Email = Email,Password = Password)
            return JsonResponse({'message':'Login Successful !','userId':user.id,'userName':user.FullName},status = 200)
        
        except:
            return JsonResponse({'message':'Invalid Credentials'},status=400)
        
# add expense API 
@csrf_exempt        
def add_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body) #convert json into python data 
        print(data)
        ExpenseDate = data.get('ExpenseDate')
        ExpenseItem = data.get('ExpenseItem')
        ExpenseCost = data.get('ExpenseCost')
        UserId = data.get('UserId')
        
        
        print(UserId)
        
            
        try:
            User =  UserDetail.objects.get(id = UserId) 
            Expense.objects.create(UserID  = User,ExpenseDate = ExpenseDate,ExpenseItem = ExpenseItem,ExpenseCost = ExpenseCost )
            print('Done')
            return JsonResponse({"message": 'Expense Added Successfully ..'},status = 201)
        except:
            return JsonResponse({'message':'somethig went wronge..'},request  = 400)
            
        
        
        
# manage expense API
@csrf_exempt
def manage_expense(request, UserId):
    if request.method == 'GET':
        # Fetch all expenses for that user
        expenses = Expense.objects.filter(UserID_id=UserId).values()

        # Convert QuerySet to list
        expense_list = list(expenses)

        if len(expense_list) == 0:
            return JsonResponse({"message": "No expenses found"}, safe=False)

        print(expense_list)
        return JsonResponse(expense_list, safe=False)




# edit Button
@csrf_exempt  #Ye basically kehta hai Django ko: “Bhai, is view me CSRF check mat karna, allow sab requests”.
def edit_expense(request, Id):
    try:
        expense = Expense.objects.get(id=Id)
    except Expense.DoesNotExist:
        return JsonResponse({"error": "Expense not found"}, status=404)

    if request.method == 'PUT':  # React sends PUT for editing
        data = json.loads(request.body) #convert into python data
        print(data)
        expense.ExpenseDate = data.get('ExpenseDate')
        expense.ExpenseItem = data.get('ExpenseItem',)
        expense.ExpenseCost = data.get('ExpenseCost',)

        expense.save()

        return JsonResponse({
            "id": expense.id,
            "ExpenseDate": expense.ExpenseDate,
            "ExpenseItem": expense.ExpenseItem,
            "ExpenseCost": expense.ExpenseCost
        })

    return JsonResponse({"error": "Invalid request method"}, status=400)


# delete_expense
@csrf_exempt
def delete_expense(request,Id):
    obj = Expense.objects.get(id = Id)
    print(obj.ExpenseItem)
    
    if request.method == 'DELETE':
        obj.delete()
        message = f'{obj.ExpenseItem} deleted successfully'
    else:
        message = 'ther is some Error ... '
    
    return JsonResponse({'message':message})

# change password
@csrf_exempt
def change_password(request, UserName):
    if request.method == 'POST':
        try:
            user = UserDetail.objects.get(FullName=UserName)
            print(user)
        
            data = json.loads(request.body)
            new_password = data.get('newpassword')

            if not new_password:
                return JsonResponse({'message': 'New password required'}, status=400)
            current_password = user.Password

            user.Password = new_password
            user.save()
            return JsonResponse({
                'message': 'Password changed successfully 😊',
                'current_password': current_password   # ✅ this is the change
            })

        except UserDetail.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)

# forget password
@csrf_exempt
def forgot_password(request, UserName):
    if request.method == 'GET':
        try:
            user = UserDetail.objects.get(FullName=UserName)
            return JsonResponse({
                'current_password': user.Password  # demo only, unsafe in real apps
            })
        except UserDetail.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
    else:
        return JsonResponse({'message': 'Only GET requests allowed'}, status=405)
