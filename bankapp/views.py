from datetime import date
from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from .models import *
import random
from faker import Faker


def home(request):
    return render(request,'home.html')

def register(request):
    print("register function called")

    # superuser_name = list(user.objects.filter(
    #     is_superuser=True).values_list('username'))
    # context = {
    #     'name': superuser_name[0][0]
    # }

    if request.method == "POST":
        data=request.POST

        first_name=data.get("first_name")
        last_name=data.get("last_name")
        email=data.get("email")
        age = data.get("age")
        addhar_number=data.get("addhar_number")
        pan_number=data.get('pan_number')
        password=data.get('password')
        confirm_password=data.get('confirm_password')
        account_type=data['account_type']

        # generate some random account number of length 10
        account_number=''
        while(len(account_number) != 10):
            account_number=("".join(str(random.randint(0,9)) for _ in range(10)))
        account_number=int(account_number)

        account_balance=3000

        if password == confirm_password:
            # print("correct password entered")

            user_object =user.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            email=email,
            addhar_number=addhar_number,
            pan_number=pan_number,
            password=password,
            confirm_password=confirm_password,
            account_type=account_type,
            account_number=account_number,
            account_balance=account_balance,
            )

            # creating the card details for this user 
            fake=Faker()
            expiry_date = fake.date_between(start_date='+1y', end_date='+4y')
            minimum = pow(10, 9)
            maximum = pow(10, 10)-1
            card_number = random.randint(minimum, maximum)
            cvv_number=random.randint(100,999)
            card =card_details.objects.create(
                customer=user_object,card_number=card_number,expiry_date=expiry_date,
                cvv_number=cvv_number
            )

            # genearting the account status 
            balance=0
            if account_type == 'saveing':
                balance=3000
            else: 
                balance=0
            account=account_status.objects.create(
                account_holder=user_object,total_balance=balance,current_balance=3000
            )
            account.save()

            # generating recurring account details
            ammount=random.randint(5000,6000)
            today=date.today()
            lapse=Faker()
            payment_date=date.today()
            rec_account=reccuring_account_status.objects.create(
                holder=user_object,payment_date=payment_date,ammount=ammount
            )
            rec_account.save()
            return redirect('/')

        
        else: 
            print("password incorrect")
            # messages.info(request,'Password does not match')
            return redirect('register')
    
    return render(request,'registration.html')


# def customer_login(request):
#     if request.method == "POST":
#         rec_list=[]
#         account_holder_names=[]

def login(request):
    if request.method =="POST":
        # import pdb; pdb.set_trace()
        email=request.POST.get("email")
        password=request.POST.get("password")

        # print(email,password)

        user_object=user.objects.all()
        # card_number = card_details.objects.all()
        # account_person = account_status.objects.all()
        # recc_account_details = reccuring_account_status.objects.all()


        account_number=None
        for dbuser in user_object:
            # import pdb; pdb.set_trace()
            if email == dbuser.email and password == dbuser.password:
                print("login successful")
                account_number= dbuser.account_number
                break
            else: 
                print("login unsuccessful")
                # return redirect('/login')
        
        user_logined=user.objects.get(account_number=account_number)
        user_details= {
            'full_name': user_logined.first_name  + " "+user_logined.last_name,
            'account_number': user_logined.account_number,
            'account_type': user_logined.account_type
        }
        # full_name = user_logined.first_name  + " "+user_logined.last_name
        # account_number=user_logined.account_number
        # account_type=user_logined.account_type
        
        user_card_details=card_details.objects.all()
        card={}
        for user_card in user_card_details:
            if user_card.customer.account_number == account_number:
                card['card_number'] = user_card.card_number
                card['cvv_number'] = user_card.cvv_number
                card['expiry_date'] = user_card.expiry_date
                break

        user_account_status=account_status.objects.all()
        logined_user_account_status={}
        for user_account in user_account_status:
            if user_account.account_holder.account_number == account_number:
                logined_user_account_status['total_balance']=user_account.total_balance
                logined_user_account_status['current_balance']=user_account.current_balance
                break 

        #creating session storage
        request.session['user_details']=user_details
        request.session['full_name']=user_details.get('full_name')
        request.session['card']=[card["card_number"],card["cvv_number"]]
        request.session['account_staus']=logined_user_account_status

        return redirect('/dashboard')

    return render(request,'login.html')


def dashboard(request):

    print(request.session.get('full_name'))
    context={
        'full_name':request.session.get('user_details').get('full_name'),
        'account_number':request.session.get('user_details').get('account_number'),
        'account_type':request.session.get('user_details').get('account_type'),

        'card_number':request.session.get('card')[0],
        'cvv_number':request.session.get('card')[1],

        'total_balance':request.session.get('account_staus')['total_balance'],
        'current_balance':request.session.get('account_staus')['current_balance'],
    }
    return render(request, "dashboard.html",context=context)