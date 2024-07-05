from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Bank, transactions
from .models import signUP, fd
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
import sqlite3

# Create your views here.
def admin_panel(request):
    # Get a list of all IDs present in the Bank model
    bank_acc_holder_ids = Bank.objects.values_list('id', flat=True)

    # Get all signUP objects
    all_customer_ids = signUP.objects.values_list('id', flat=True)

    # Convert bank_acc_holder_ids to a list
    bank_acc_holder_ids_list = list(bank_acc_holder_ids)

    # Get the remaining IDs that are not in bank_acc_holder_ids
    remaining_customer_ids = set(all_customer_ids) - set(bank_acc_holder_ids_list)

    # Retrieve the signUP objects corresponding to the remaining IDs
    remaining_customers = signUP.objects.filter(id__in=remaining_customer_ids)

    context = {'customer': remaining_customers}
    return render(request, 'admin_panel.html', context)

    # customer = signUP.objects.all()
    #     context = {'customer': customer}
    #     return render(request, 'admin_panel.html', context)

def index_signup(request): 
    
    template = loader.get_template('index_signup.html')  # it only loads template
    return HttpResponse(template.render())

def index_login(request): 
    
    template = loader.get_template('index_login.html')  # it only loads template
    return HttpResponse(template.render())

def main(request): 
    
    template = loader.get_template('index.html')  # it only loads template
    return HttpResponse(template.render())

def viewaccounts(request): 
    template = loader.get_template('admin_panel.html')  # it only loads template
    return HttpResponse(template.render())
   
def addaccounts(request, user_id):  # this function adding the new account
    user = signUP.objects.get(id=user_id)
    if (Bank.objects.filter(id=user_id).exists()):
        return HttpResponse("Account already exists")
    else:
        return render(request, 'createAccount.html',{'user': user})
   
def listaccounts(request):   # this function is used to list the existing accounts
    customer = Bank.objects.all()
    context = {'customer': customer}
    return render(request, 'listaccount.html', context)

def withdraw(request):    # function used to load template of withdraw
    template = loader.get_template('withdraw-deposit.html')
    return HttpResponse(template.render())

def myWithdraw(request):   #function is used to withdraw money from balance.
    a = request.GET['t1']
    b = request.GET['t2']
    # print("-------")
    
    try:
        m = Bank.objects.get(accountno=a)
        user_id = m.id
        m.balance = int(m.balance) - int(b)
        m.save()
        t = transactions(user_id=user_id,AccountNo = a,t_type = 'Debit',amount = b, balance= m.balance)
        t.save()

        # Calculate the total amount withdrawn
       
        return HttpResponse('Money withdrawn succesfully')
    except Bank.DoesNotExist:
        return HttpResponse('No Account found')
    

def deposit(request):   # fn is used to load template of deposit
    template = loader.get_template('deposit.html')
    return HttpResponse(template.render())
  
def myDeposit(request):  # fn is used for deposit money in balance of sepicific account
    a = request.GET['t1']
    b = request.GET['t2']
    # print("-------")
   
    try:
        m = Bank.objects.get(accountno=a)
        user_id = m.id
        m.balance = int(m.balance) + int(b)
        m.save()
        t = transactions(user_id=user_id,AccountNo = a,t_type = 'Credit',amount = b, balance= m.balance)
        t.save()
        return HttpResponse('Money Deposited succesfully')
    except Bank.DoesNotExist:
        return HttpResponse('No Account found')

def storedetails(request):   # this fn is stronging details of new acoount formed in database
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        account_number = request.GET.get('account_number')
        user_name = request.GET.get('user_name')
        balance = request.GET.get('balance')
        if (Bank.objects.filter(id=user_id).exists()):
            return HttpResponse("Account already exists")
        
        else:    
            bank = Bank(
                id=user_id,
                accountno=account_number,
                name=user_name,
                balance=balance
            )
            bank.save()
            return HttpResponse("Account added successfully!")
    else:
        return HttpResponse("Invalid request method")    

def delete(request):  # fn is used to load delete template
    template = loader.get_template('delete.html')
    return HttpResponse(template.render())
    
def myDelete(request):   #fn is acctually deleting the account specified.
    a = request.GET['t1']
    bank_records = Bank.objects.filter(accountno=a)
    if bank_records.exists():
                # Delete the first record found
        bank_record = bank_records.first()
        bank_record.delete()
        return HttpResponse('Account deleted sucessfully')
    else:
        return HttpResponse('No such account found')

def update(request):   # fn is loading the update template
    template = loader.get_template('update.html')
    return HttpResponse(template.render())

def myUpdate(request):   # fn is used to change the value which admin wants to change.
    a = request.GET['t1']
    b = request.GET['t2']

    try: 
        member = Bank.objects.get(accountno = a)
        member.name = b
        

        member.save()
        return HttpResponse('Account updated succesfully')
    except Bank.DoesNotExist:
        return HttpResponse('No Account found')
    

#  login signup views are below this line...

def signUp_cust(request):  # fn is used to load signup template.
    template = loader.get_template('signup_customer.html')
    return HttpResponse(template.render())  

def login_cust(request):  # fn is used to load the login template.
    template = loader.get_template('index_login.html')
    return HttpResponse(template.render()) 

def mylogin_cust(request):  # fn is used to check the the login details. if Admin login then he is redirected to another page and for customer is redirected to different template.
    a= request.GET['t2']
    b= request.GET['t3']
    m = signUP.objects.get(emailid=a, password=b)
    if (a == m.emailid and b == m.password):
        if(m.User_type=='Admin'):
            request.session['id'] = m.id
            # Get a list of all IDs present in the Bank model
            bank_acc_holder_ids = Bank.objects.values_list('id', flat=True)

            # Get all signUP objects
            all_customer_ids = signUP.objects.values_list('id', flat=True)

            # Convert bank_acc_holder_ids to a list
            bank_acc_holder_ids_list = list(bank_acc_holder_ids)

            # Get the remaining IDs that are not in bank_acc_holder_ids
            remaining_customer_ids = set(all_customer_ids) - set(bank_acc_holder_ids_list)

            # Retrieve the signUP objects corresponding to the remaining IDs
            remaining_customers = signUP.objects.filter(id__in=remaining_customer_ids)

            context = {'customer': remaining_customers}
            return render(request, 'admin_panel.html', context)
                        # return render(request, 'form1.html')
    
        elif(m.User_type=='customer'):
            request.session['id']= m.id
            user_id = request.session.get('id')
        if user_id:
            user = signUP.objects.get(id=user_id)
            user1 = Bank.objects.get(id=user_id)
            return render(request, 'login_success.html', {'user': user,'user1': user1})

def userhome(request):
        user_id = request.session.get('id')
        if user_id:
            user = signUP.objects.get(id=user_id)
            user1 = Bank.objects.get(id=user_id)
            return render(request, 'login_success.html', {'user': user,'user1': user1})         

def viewprofile(request):  # fn is used to load viewprofile template and to show the stored value in html page.
    user_id = request.session.get('id')
    if user_id:
        user = signUP.objects.get(id=user_id)
        user1 = Bank.objects.get(id=user_id)
        return render(request, 'viewprofile.html', {'user': user,'user1': user1})
    
def editprofile(request): # fn is used to load editprofile.html.
    user_id = request.session.get('id')
    if user_id is not None:
        user = signUP.objects.get(id=user_id)
        return render(request, 'editprofile.html',{'user':user})

def update_editprofile(request): # fn is used to edit the values in respected feild.
    user_id = request.session.get('id')
    if user_id is not None:
        a= request.GET.get('t1')    
        b= request.GET.get('t2')    
        c= request.GET.get('t3')
        try:
            u = signUP.objects.get(id=user_id)
            u.username = a
            u.emailid=b
            u.phoneNo=c
            u.save()
            return redirect('viewprofile')
        except signUP.DoesNotExist:
            return HttpResponse('userprofile not exists')
    else:
        return HttpResponse('id not found')


def transaction(request):  # fn is used to show values of transactions of customer on transactions.html
    # print("Session ID:", request.session.get('id'))
    user_id = request.session.get('id')
    if user_id:
        try:
            user = Bank.objects.get(id=user_id)
            t = transactions.objects.filter(user_id=user_id)
            total_credit_amount = t.filter(t_type='Credit').aggregate(Sum('amount'))['amount__sum']
            total_credit_amount = total_credit_amount if total_credit_amount else 0
            
            total_debit_amount = t.filter(t_type='Debit').aggregate(Sum('amount'))['amount__sum']
            total_debit_amount = total_debit_amount if total_debit_amount else 0

            # context = {'t': t}
            return render(request, 'transactions.html', {'t': t, 'user':user, 'total_credit_amount': total_credit_amount, 'total_debit_amount': total_debit_amount})
        except transactions.DoesNotExist:
            # Handle case where transaction with the given ID doesn't exist
            return HttpResponse("Transaction not found.")
        
def Deposits(request):    # function used to load template of withdraw
    user_id = request.session.get('id')
    if user_id:
        u = Bank.objects.get(id=user_id)
        return render (request, 'user_deposits.html', {'u':u})

def create_fd(request):
    user_id = request.session.get('id')
    # date_time = timezone.now()
    if user_id:
        u = Bank.objects.get(id=user_id)
        return render (request, 'create_fd.html', {'u':u})
    #  template = loader.get_template('show_fd.html')
    #  return HttpResponse(template.render())
    
def show_fd(request):
    user_id = request.session.get('id')
    # date_time = timezone.now()
    if user_id:
        u = fd.objects.filter(user_id=user_id)
        return render (request, 'show_fd.html', {'u':u})

    #  template = loader.get_template('show_fd.html')
    #  return HttpResponse(template.render())

def fd_details(request):
    user_id = request.session.get('id')
    if user_id:
        u = Bank.objects.get(id=user_id)
        user_id = u.id
        

        a = int(request.GET.get('t2'))   #fd amount
        start_date_str = request.GET.get('t3')   # Use .get() instead of ()
        maturity_date_str = request.GET.get('t5')   #maturity date

        c = int(request.GET.get('t4'))   #interest rate

        # d = request.GET.get('t5')   #time zone
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        maturity_date = datetime.strptime(maturity_date_str, '%Y-%m-%d')

        time_period = (maturity_date - start_date).days
        time_in_yrs =  (time_period/365)
        principal = a   # fd amount
        rate = c      # rate of interest
        n = 1           #number of times interest rate applied in a year
    maturity_amount = (principal * (1 + (rate/100)/n) ** (n * time_in_yrs))
    
    if a<u.balance:        
        FD = fd( user_id= user_id,
                fd_amount= a, 
                time_period = time_period, 
                int_rate = rate,  
                mat_amount = maturity_amount,
                maturity_date = maturity_date_str)
        FD.save()
        
        u.balance -= int(a)
        u.save()
        t = transactions(user_id=user_id, 
                        AccountNo = u.accountno, 
                        t_type="Debit", 
                        amount = a, 
                        balance = u.balance,
                        )
        t.save()
        return HttpResponse("A FD in your account has been added")
    else:
        return HttpResponse("Balance is low")
       
def logout(request): 
    request.session.flush()  #  flush fn is used to delete the active session.. we also used pop() method but it didn't work.
    return redirect('main')  


def storedetails_cust_sign(request):  # store details of signup page.
    cust_sign = signUP(username=request.GET['t1'], phoneNo=request.GET['t2'],emailid=request.GET['t3'],password=request.GET['t4'])
    confpassword=request.GET['t5']
    if(cust_sign.username=='' or cust_sign.phoneNo=='' or cust_sign.emailid=='' or cust_sign.password==''):
        return HttpResponse('feilds cannot be blank')
    elif(cust_sign.password != confpassword):
        return HttpResponse('password dont match')
    else:
        cust_sign.User_type = 'customer'
        cust_sign.save()
        template = loader.get_template('index_login.html')
        return HttpResponse(template.render())
