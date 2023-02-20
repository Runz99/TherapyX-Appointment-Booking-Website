from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta
from .models import *

# Create your views here.


def home(request):
    context = {}
    return render(request, 'base/home.html', context)

# ========================================= LOGIN / LOGOUT / REGISTRATION FUNCTIONs ================================================
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Account does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #return redirect('home')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context={'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "an error has occured during registration")
    context = {'form':form}
    return render(request, 'base/register_user.html', context)



# ================================================ SESSION BOOKING FUNCTIONS =====================================================
@login_required(login_url='login')
def bookingPage(request):
    weekdays = validWeekday(22)
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == "POST":
        appt_day = request.POST.get('appt_day')

        #store day in django session
        request.session['appt_day'] = appt_day

        return redirect('bookingSubmit')
    
    context = {'weekdays': weekdays, 'validateWeekdays': validateWeekdays }
    return render(request, 'base/book_session.html', context)

def bookAdmin(request):
    # clientsNum = User.objects.count()
    clients = User.objects.all()
    weekdays = validWeekday(22)
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == "POST":
        appt_day = request.POST.get('appt_day')
        user = request.POST.get('userid')
        #print(user)
        #store day in django session
        request.session['userid'] = user
        request.session['appt_day'] = appt_day

        return redirect('bookingAdminSubmit')

    context = {'clients':clients,'weekdays': weekdays, 'validateWeekdays': validateWeekdays }
    return render(request, 'base/book_admin.html', context)

def bookingSubmit(request):
    user = request.user
    times = ['10:00 AM', '11:00 AM', '12:00 AM', '2:00 PM','3:00 PM','4:00 PM','5:00 PM','6:00 PM','7:00 PM','8:00 PM']
    # opening_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    maxDate = deltatime.strftime('%Y-%m-%d')

    day = request.session.get('appt_day')
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = daytoWeekday(day)
        # date = "Thursday"
        if day >= minDate and day <= maxDate:
            if date=="Monday" or date=='Tuesday' or date=="Wednesday" or date=="Thursday" or date=='Friday':
                if Appointment.objects.filter(day=day).count() < 11:
                    if Appointment.objects.filter(day=day, time=time).count() < 1:
                        AppointmentForm = Appointment.objects.get_or_create(
                                    user = user,
                                    day = day,
                                    time = time,
                                )
                        messages.success(request, "Appointment Saved")
                        return redirect('home')
                    else:
                        messages.success(request, "The selected time has been reserved before")
                else:
                    messages.success(request, "The selected day is full")
            else:
                messages.success(request, "Services are not available on this date")
        else:
            messages.success(request, "The selected date is not within booking period")
        
    context = {'times': hour}
    return render(request, 'base/bookingSubmit.html', context)

def bookingAdminSubmit(request):
    times = ['10:00 AM', '11:00 AM', '12:00 AM', '2:00 PM','3:00 PM','4:00 PM','5:00 PM','6:00 PM','7:00 PM','8:00 PM']
    # opening_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    maxDate = deltatime.strftime('%Y-%m-%d')

    userid = request.session.get('userid')
    user = User.objects.get(username = userid)
    day = request.session.get('appt_day')
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = daytoWeekday(day)
        # date = "Thursday"
        if day >= minDate and day <= maxDate:
            if date=="Monday" or date=='Tuesday' or date=="Wednesday" or date=="Thursday" or date=='Friday':
                if Appointment.objects.filter(day=day).count() < 11:
                    if Appointment.objects.filter(day=day, time=time).count() < 1:
                        AppointmentForm = Appointment.objects.get_or_create(
                                    user = user,
                                    day = day,
                                    time = time,
                                )
                        messages.success(request, "Appointment Saved")
                        return redirect('home')
                    else:
                        messages.success(request, "The selected time has been reserved before")
                else:
                    messages.success(request, "The selected day is full")
            else:
                messages.success(request, "Services are not available on this date")
        else:
            messages.success(request, "The selected date is not within booking period")
        
    context = {'times': hour}
    return render(request, 'base/bookingSubmit.html', context)

# ======================================================= ACCOUNT PAGE FUNCTIONS ==================================================
@login_required(login_url='login')
def account(request):
    user = request.user
    # FOR USER PANEL
    appointments = Appointment.objects.filter(user=user).order_by('day','time')
    # FOR ADMIN PANEL
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')
    startDate = '2023-02-16'
    lastDate = today - timedelta(days=1)
    prevs = Appointment.objects.filter(day__range=[startDate, lastDate]).order_by('day', 'time')
    context = {
        'user':user,
        'appointments':appointments,
        'items':items,
        'prevs':prevs,
    }
    return render(request, 'base/account.html', context)

# ======================================================= CONTACT PAGE FUNCTIONS ==================================================

def contactPage(request):
    context = {}
    return render(request, 'base/contact.html', context)


# ======================================================= ACCESSORY FUNCTIONS =====================================================
def clientList(num):
    clientele = []
    for m in range(0,num):
        username = User.objects.filter(id=m).values('id','username')
        clientele.append(username)
    return clientele

def daytoWeekday(x):
    z = datetime.strptime(x, '%Y-%m-%d')
    y = z.strftime('%A')
    return y


def checkTime(times,day):
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def validWeekday(days):
    today = datetime.now()
    weekdays = []
    for i in range(0,days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        opening_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if y in opening_days:
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays

def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays