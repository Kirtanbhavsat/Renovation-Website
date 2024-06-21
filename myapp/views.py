from django.shortcuts import render,redirect
from .models import registration,services,booking,contactus,feedback
from django.contrib import messages
# Create your views here.

def aboutpage(request):
    return render(request,"about.html")

def contactpage(request):
    return render(request,"contact.html")

def contactdata(request):
    u_name = request.POST.get("name")
    u_email = request.POST.get("useremail")
    u_phone = request.POST.get("userphone")
    u_sub = request.POST.get("subject")
    u_meg = request.POST.get("message")

    contactinfo = contactus(name=u_name,uemail=u_email,phone=u_phone,subject=u_sub,message=u_meg)
    contactinfo.save()

    return render(request,"index.html")
def homepage(request):
    return render(request,"index.html")
def signuppage(request):
    return render(request,"signup.html")

def insertinfo(request):
    uname = request.POST.get("rname")
    upic = request.FILES["rpic"]
    ugen = request.POST.get("gender")
    umail = request.POST.get("uemail")
    uno = request.POST.get("mno")
    udob = request.POST.get("rdob")
    uadd = request.POST.get("add")
    rtype = request.POST.get("role")
    upass = request.POST.get("pass")

    storinfo = registration(name=uname,dp=upic,gender=ugen,email=umail,phone_no=uno,dob=udob,address=uadd,r_type=rtype,password=upass)
    storinfo.save()

    return render(request,"login.html")

def loginpage(request):
    return render(request,"login.html")

def servicepage(request):
    fetchser = services.objects.all()
    context = {
        'data':fetchser
    }
    return render(request,"services.html",context)

def singleservice(request , sid ):
    fetchsingleser = services.objects.get(id=sid)
    context = {
        'data': fetchsingleser
    }

    return render(request,"single-service.html",context)

def addservices(request):
    return render(request,"addservices.html")

def manageservice(request):
    uid = request.session["logid"]
    fetchserdata = services.objects.filter(email_id=uid)
    context = {
        'data':fetchserdata
    }
    return render(request,"manageservice.html",context)

def deletepage(request , id):
    fetchdata = services.objects.get(id=id)
    fetchdata.delete()
    return redirect("/manageservice")

def insertser(request):
    sname = request.POST.get("ser_type")
    simg = request.FILES["serimg"]
    spri = request.POST.get("serprice")
    sdesc = request.POST.get("serdesc")
    coname = request.session["logid"]

    storser = services(sname=sname,simg=simg,sprice=spri,sdesc=sdesc,email_id=registration(id=coname))
    storser.save()

    return redirect("/manageservice")

def checkuserinfo(request):

    useremail = request.POST.get("mail")
    userpass = request.POST.get("passcod")

    try:
        checkinfo = registration.objects.get(email=useremail,password=userpass)
        request.session["logid"] = checkinfo.id
        request.session["logemail"] = checkinfo.email
        request.session["logname"] = checkinfo.name
        request.session["rol"] = checkinfo.r_type
        request.session.save()
    except:
        checkinfo = None

    if checkinfo is not None:
        return redirect("/")
    else:
        messages.error(request,"Invalid Email or Password Please Try Again !")

    return render(request,"login.html")

def logout(request):

    try:
        del request.session["logid"]
        del request.session["logemail"]
        del request.session["logname"]
        del request.session["rol"]
    except:
        pass

    return render(request,"login.html")

def bookingpage(request):
    userid = request.session["logid"]
    ser_id = request.POST.get("sid")
    address = request.POST.get("address")
    contact = request.POST.get("phone")
    sdate = request.POST.get("startdate")
    paytype = request.POST.get("payment")


    storedata = booking(userid=registration(id=userid),serviceid=services(id=ser_id),address=address,contact=contact,start_date=sdate,pay_type=paytype,b_status=0)
    storedata.save()
    messages.success(request,"Booking done Successfully")
    return redirect("/booking")

def managebooking(request):
    cid = request.session["logid"]
    fetchsids = services.objects.filter(email_id=cid)
    fetchserdata = booking.objects.filter(serviceid__in = fetchsids)
    print(fetchserdata)
    context = {
        'data':fetchserdata
    }
    return render(request,"managebooking.html",context)

def rejectbooking(request , id):
    fetchbookingdetail = booking.objects.get(id=id)
    fetchbookingdetail.b_status = 1 # Reject
    fetchbookingdetail.save()

    username = fetchbookingdetail.userid.email
    msg = "hello, Your booking is cancelled  By Contractor, Please try again !"

    from django.core.mail import send_mail

    send_mail(
        'Your booking is cancelled',
        msg,
        'krushanuinfolabz@gmail.com',
        [username],
        fail_silently=False,
    )
    print('Mail sent')
    messages.info(request, 'booking is cancelled')
    return redirect("/managebooking")


def book(request):
    uid = request.session["logid"]
    fetchserdata = booking.objects.filter(userid=uid)
    context = {
        'bookdata': fetchserdata
    }
    return render(request,"booking.html",context)

def cancelbooking(request , id):
    fetchbookingdetail = booking.objects.get(id=id)
    fetchbookingdetail.b_status = 2 # Cancelled by User
    fetchbookingdetail.save()

    username = fetchbookingdetail.userid.email
    msg = "hello, Your booking is cancelled  By You, Please Book another Service !"

    from django.core.mail import send_mail

    send_mail(
        'Your booking is cancelled',
        msg,
        'krushanuinfolabz@gmail.com',
        [username],
        fail_silently=False,
    )
    print('Mail sent')
    messages.info(request, 'booking is cancelled')
    return redirect("/booking")


def feedbackpage(request,id):
    context = {
        "data":id
    }
    return render(request,"feedback.html",context)

def insertfeed(request):
    fid = request.POST.get("bid")
    rat = request.POST.get("rating")
    com = request.POST.get("comment")

    datafeed = feedback(book_id=booking(id=fid),rating=rat,comment=com)
    datafeed.save()

    return redirect("/booking")

def forgotpage(request):
    return render(request,"forgotpassword.html")

def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST['uemail']
        try:
            user = registration.objects.get(email=username)

        except registration.DoesNotExist:
            user = None
        #if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  #we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################


            msg = "hello here it is your new password  "+password   #this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'krushanuinfolabz@gmail.com',
                [username],
                fail_silently=False,
            )

            #now update the password in model
            cuser = registration.objects.get(email=username)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect("/login")

        else:
            messages.info(request, 'This account does not exist')
    return redirect("/login")

def editservice(request,id):
    getdata = services.objects.get(id=id)
    context = {
        "data":getdata
    }
    return render(request,"editservice.html",context)

def updatedata(request):
    sname = request.POST.get("ser_type")
    simg = request.FILES["serimg"]
    spri = request.POST.get("serprice")
    sdesc = request.POST.get("serdesc")
    sid = request.POST.get("sid")

    getdat=services.objects.get(id=sid)
    getdat.sname=sname
    getdat.sprice=spri
    getdat.sdesc=sdesc
    getdat.simg=simg
    getdat.save()

    messages.success(request, "Successfully Edited")

    return redirect("/manageservice")