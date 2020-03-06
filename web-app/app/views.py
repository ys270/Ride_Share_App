from django.shortcuts import render
from .models import Users, Rides
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
import hashlib
from django.core.mail import send_mass_mail
from django.db.models import Q
from datetime import datetime
cur_time = datetime.now()

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    return str(password)

def register(request):
    if request.method=='POST':
        data=request.POST
        email=data.get("email")
        password=data.get("password")
        Users.objects.create(
            email=email,
            password=setPassword(password),
        )
        return HttpResponseRedirect('/app/login/')
    return render(request,"app/register.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        e = Users.objects.filter(email=email).first()
        if e:
            now_password=setPassword(password)
            db_password = e.password
            if now_password == db_password:
                e.is_loggedin=True
                e.save()
                response = HttpResponseRedirect('/app/index/')
                request.session["user_id"] = e.pk
                return response
            else:
                return render(request, "app/login.html",{'hello': 'wrong password!'})
        else:
            return render(request, "app/login.html",{'hello': 'email not record!'})
    return render(request, "app/login.html")

def index(request):
    user_id = request.session["user_id"]
    user = Users.objects.filter(pk=user_id).first()
    if request.method == 'POST':
        user.is_loggedin=False
        user.save()
        response = HttpResponseRedirect('/app/login/')
        del request.session["user_id"]
        return response
    if not user.is_driver:
        return render(request,"app/index1.html")
    else:
        return render(request,"app/index2.html")

def request_ride(request):
    user_id = request.session["user_id"]
    user = Users.objects.filter(pk=user_id).first()
    if request.method == 'POST':
        owner = user.email
        data = request.POST
        owner_party_size = int(data.get("owner_party_size"))
        car_seat = int(data.get("car_seat"))
        is_sharable = data.get("is_sharable")
        destination = data.get("destination")
        arrival_time = data.get("arrival_time")
        arr_time = datetime.strptime(arrival_time, '%Y-%m-%dT%H:%M')
        if arr_time < cur_time or car_seat < owner_party_size:
            return HttpResponseRedirect('/app/owner_edit_fail/')
        remaining_size = car_seat-owner_party_size
        Rides.objects.create(
            owner = owner,
            owner_party_size = owner_party_size,
            car_seat = car_seat,
            is_sharable = is_sharable,
            destination = destination,
            arrival_time = arrival_time,
            remaining_size = remaining_size,
        )
        return HttpResponseRedirect('/app/request_ride_success/')
    return render(request, "app/request_ride.html")

def request_ride_success(request):
    user_id = request.session["user_id"]
    user = Users.objects.filter(pk=user_id).first()
    if request.method == 'POST':
        return HttpResponseRedirect('/app/index/')
    return render(request, "app/request_ride_success.html")

def request_ride_fail(request):
    user_id = request.session["user_id"]
    user = Users.objects.filter(pk=user_id).first()
    if request.method == 'POST':
        return HttpResponseRedirect('/app/index/')
    return render(request, "app/owner_edit_fail.html")

def join_ride_success(request):
    user_id = request.session["user_id"]
    user = Users.objects.filter(pk=user_id).first()
    if request.method == 'POST':
        return HttpResponseRedirect('/app/index/')
    return render(request, "app/join_ride_success.html")

def join_ride(request):
    return render(request, 'app/join_ride.html')

def select_sharer_ride(request):
    sharer_id = request.session["user_id"]
    sharer_session = Users.objects.filter(pk=sharer_id).first()
    email = str(sharer_session.email)
    if request.method == 'POST':
        data = request.POST
        ride_pk = data.get("ride_pk")
        choose_ride = 'False'
        choose_ride = data.get("choose_ride")
        sharer_party_size=int(data.get("sharer_party_size"))
        if choose_ride == 'True':
            ride = Rides.objects.filter(pk=ride_pk).first()
            ride.remaining_size = ride.remaining_size - sharer_party_size
            if ride.sharer:
                ride.sharer.append(email)
            else:
                ride.sharer = [email]
            if ride.sharer_party_size:
                ride.sharer_party_size.append(sharer_party_size)
            else:
                ride.sharer_party_size = [sharer_party_size]
            ride.save()
            return HttpResponseRedirect('/app/index/')
        earlist_arrival_time=data.get("earlist_arrival_time")
        latest_arrival_time=data.get("latest_arrival_time")
        latest_arr_time = datetime.strptime(latest_arrival_time, '%Y-%m-%dT%H:%M')
        if latest_arr_time < cur_time:
            return HttpResponse('The time window should not be earlier than now!')
        destination=data.get("destination")
        ride_list = Rides.objects.filter(~Q(owner=email))
        if ride_list:
            ride_list = ride_list.filter(arrival_time__lte=latest_arrival_time, arrival_time__gte=earlist_arrival_time,
                                         destination=destination, is_confirmed=False, is_complete=False,
                                         is_sharable=True, remaining_size__gte=sharer_party_size)
        if ride_list:
            ride_list = ride_list.filter(~Q(sharer__contains=[email]))
        context = {'ride_list': ride_list, 'sharer_party_size':sharer_party_size}
        if ride_list:
            return render(request, 'app/select_sharer_ride.html', context)
        else:
            return HttpResponse("No such kind of ride!")

def my_rides_as_owner(request):
    return render(request, 'app/my_rides_as_owner.html')

def owner_open(request):
    owner_id = request.session["user_id"]
    owner = Users.objects.filter(pk=owner_id).first()
    email = owner.email
    ride_list = Rides.objects.filter(owner=email, is_confirmed=False, is_complete=False)
    if ride_list:
        context = {'ride_list': ride_list}
        return render(request, 'app/owner_open.html', context)
    else:
        return HttpResponse("You have no owned confirmed rides!")

def owner_open_detail(request):
    user_id = request.session["user_id"]
    user = Users.objects.filter(pk=user_id).first()
    if request.method == 'POST':
        data = request.POST
        ride_pk = data.get("ride_pk")
        ride = Rides.objects.filter(pk=ride_pk).first()
        ride.save()
        save_edit = 'False'
        save_edit = data.get("save_edit")
        """sharer = data.get("sharer")"""
        if save_edit == 'True':
            owner = user.email
            owner_party_size = int(data.get("owner_party_size"))
            car_seat = int(data.get("car_seat"))
            is_sharable = data.get("is_sharable")
            destination = data.get("destination")
            arrival_time = data.get("arrival_time")
            remaining_size = car_seat - owner_party_size
            arr_time = datetime.strptime(arrival_time, '%Y-%m-%dT%H:%M')
            if remaining_size<0 or arr_time < cur_time:
                return HttpResponseRedirect('/app/owner_edit_fail/')
            ride.owner = owner
            ride.owner_party_size = owner_party_size
            ride.car_seat = car_seat
            ride.is_sharable = is_sharable
            ride.destination = destination
            ride.arrival_time = arrival_time
            ride.remaining_size = remaining_size
            ride.save()
            return HttpResponseRedirect('/app/index/')
        context = {'ride': ride}
        return render(request, "app/owner_open_detail.html",context)

def owner_edit_fail(request):
    user_id = request.session["user_id"]
    user = Users.objects.filter(pk=user_id).first()
    if request.method == 'POST':
        return HttpResponseRedirect('/app/index/')
    return render(request, "app/owner_edit_fail.html")

def owner_confirmed(request):
    owner_id = request.session["user_id"]
    owner = Users.objects.filter(pk=owner_id).first()
    email = owner.email
    ride_list = Rides.objects.filter(owner=email, is_confirmed=True, is_complete=False)
    if ride_list:
        context = {'ride_list': ride_list}
        return render(request, 'app/owner_confirmed.html', context)
    else:
        return HttpResponse("You have no owned rides!")

def owner_confirmed_detail(request):
    if request.method == 'POST':
        data = request.POST
        ride_pk = data.get("ride_pk")
        ride = Rides.objects.filter(pk=ride_pk).first()
        driver = Users.objects.filter(email=ride.driver).first()
        ride.save()
        context = {'ride': ride, 'driver': driver}
        return render(request, "app/owner_confirmed_detail.html", context)

def my_rides_as_sharer(request):
    return render(request, 'app/my_rides_as_sharer.html')

def sharer_confirmed(request):
    owner_id = request.session["user_id"]
    owner = Users.objects.filter(pk=owner_id).first()
    email = owner.email
    ride_list = Rides.objects.filter(is_confirmed=True, is_complete=False,sharer__contains=[email])
    if ride_list:
        context = {'ride_list': ride_list}
        return render(request, 'app/sharer_confirmed.html', context)
    else:
        return HttpResponse("You have no confirmed rides!")

def sharer_quit(request):
    sharer_id = request.session["user_id"]
    sharer = Users.objects.filter(pk=sharer_id).first()
    if request.method == 'POST':
        email = sharer.email
        data = request.POST
        ride_pk = data.get("ride_pk")
        ride = Rides.objects.filter(pk=ride_pk).first()
        index = ride.sharer.index(email)
        ride.remaining_size += ride.sharer_party_size[index]
        ride.sharer.remove(email)
        ride.sharer_party_size.pop(index)
        ride.save()
        return HttpResponse("You successfully quit a ride!!!!!!")

def sharer_confirmed_detail(request):
    if request.method == 'POST':
        data = request.POST
        ride_pk = data.get("ride_pk")
        ride = Rides.objects.filter(pk=ride_pk).first()
        driver = Users.objects.filter(email=ride.driver).first()
        ride.save()
        context = {'ride': ride, 'driver': driver}
        return render(request, "app/sharer_confirmed_detail.html", context)

def sharer_open(request):
    owner_id = request.session["user_id"]
    owner = Users.objects.filter(pk=owner_id).first()
    email = owner.email
    ride_list = Rides.objects.filter(is_confirmed=False, is_complete=False,sharer__contains=[email])
    if ride_list:
        context = {'ride_list': ride_list}
        return render(request, 'app/sharer_open.html', context)
    else:
        return HttpResponse("You have no shared open rides!")

def my_rides_as_driver(request):
    driver_id = request.session["user_id"]
    driver = Users.objects.filter(pk=driver_id).first()
    email = driver.email
    ride_list = Rides.objects.filter(driver=email, is_confirmed=True, is_complete=False)
    if ride_list:
        context = {'ride_list': ride_list }
        return render(request, 'app/my_rides_as_driver.html', context)
    else:
        return HttpResponse("You have no rides!")

def driver_ride_detail(request):
    if request.method == 'POST':
        data = request.POST
        ride_pk = data.get("ride_pk")
        ride = Rides.objects.filter(pk=ride_pk).first()
        ride.save()
        complete = 'False'
        complete = data.get("is_complete")
        if complete == 'True':
            ride.is_complete = True
            ride.save()
            return HttpResponseRedirect('/app/index/')
        context = {'ride': ride}
        return render(request, "app/driver_ride_detail.html",context)


def register_as_driver(request):
    user_id = request.session["user_id"]
    user = Users.objects.filter(pk=user_id).first()
    if request.method=='POST':
        user.is_driver = True
        data=request.POST
        user.plate_id=data.get("plate_id")
        user.car_size=int(data.get("car_size"))
        user.save()
        return HttpResponseRedirect('/app/index/')
    return render(request, "app/register_as_driver.html")


def driver_search(request):
    driver_id = request.session["user_id"]
    driver = Users.objects.filter(pk=driver_id).first()
    car_size=int(driver.car_size)
    email=driver.email
    ride_list=Rides.objects.filter(~Q(owner=email),is_confirmed=False, is_complete=False, car_seat=car_size)
    if ride_list:
        ride_list=ride_list.filter(~Q(sharer__contains=[email]))
    if ride_list:
        if request.method == 'POST':
            data = request.POST
            ride_pk = int(data.get("ride_pk"))
            ride = Rides.objects.get(pk=ride_pk)
            ride.driver = driver.email
            ride.is_confirmed = True
            ride.save()
            message1 = (
                'Confirmation of Owned Ride',
                'Your Ride has been confirmed by driver:\n'
                +ride.driver+'\n'+'Information:\n'+'Destination: '+ride.destination+'\n'+'Arrival Time: '+str(ride.arrival_time)+'\n', 'shaoyue1997@gmail.com', [ride.owner])
            message2 = (
                'Confirmation of Shared Ride', 'Your Ride has been confirmed by driver:\n'
                +ride.driver+'\n'+'Information:\n'+'Destination: '+ride.destination+'\n'+'Arrival Time: '+str(ride.arrival_time)+'\n', 'shaoyue1997@gmail.com', ride.sharer)
            send_mass_mail((message1, message2), fail_silently=False)
            return HttpResponseRedirect('/app/index/')
        context = {'ride_list': ride_list}
        return render(request, 'app/driver_search_list.html', context)
    else:
        return HttpResponse("no suitable ride can be found!")

def edit_driver_information(request):
    user_id = request.session["user_id"]
    user = Users.objects.filter(pk=user_id).first()
    if request.method=='POST':
        data=request.POST
        is_driver = data.get("is_driver")
        user.is_driver=data.get("is_driver")
        user.plate_id=data.get("plate_id")
        user.car_size=int(data.get("car_size"))
        user.save()
        if is_driver =='False':
            user.plate_id = ''
            user.car_size = 0
            user.save()
        user.save()
        return HttpResponseRedirect('/app/index/')
    return render(request, "app/edit_driver_information.html")