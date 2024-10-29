from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render,redirect
import qrcode
from django.http import HttpResponse
from io import BytesIO
import qrcode
from taxi import settings
from django.core.files.base import ContentFile
import io
from datetime import datetime
import os
from .models import *
import razorpay
import smtplib
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def landing(request):
    ratings = Rating.objects.filter().order_by('-id')
    auth.logout(request)
    return render(request,"landing.html",{'ratings':ratings})


def login(request):
    auth.logout(request)
    return render(request,"login.html")


def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    try:
        ob = Login_table.objects.get(username=username, password=password)
        request.session['lid']=ob.id
        ob1=auth.authenticate(username="admin",password="admin")
        if ob1 is not None:
            auth.login(request,ob1)
        if ob.type == "admin":
            return HttpResponse('''<script>alert('Welcome');window.location='/Adminhome'</script>''')
        elif ob.type== "driver":
            try:
                driver = Driver.objects.get(LOGIN=ob)
                return HttpResponse('''<script>alert('Welcome, Driver');window.location='/Driverhome'</script>''')
            except Driver.DoesNotExist:
                return HttpResponse('''<script>alert('Driver profile not found. Please contact support.');window.location='/'</script>''')
        elif ob.type== "customer":
            try:
                customer = Customer.objects.get(LOGIN=ob)
                return HttpResponse('''<script>alert('Welcome, Customer');window.location='/view_profile'</script>''')
            except Customer.DoesNotExist:
                return HttpResponse(
                    '''<script>alert('Customer profile not found. Please contact Admin.');window.location='/'</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert('Invalid username or password');window.location='/'</script>''')



def cregister(request):
    return render(request, "cregister.html")


def cregister_post(request):
    name=request.POST['name']
    phone=request.POST['phone']
    email = request.POST['email']
    place = request.POST['place']
    post=request.POST['post']
    pin=request.POST['pin']
    password = request.POST['password']

    login_details = Login_table()
    login_details.username = email
    login_details.password = password
    login_details.type = 'customer'
    login_details.save()

    profile = Customer()
    profile.LOGIN = login_details
    profile.name = name
    profile.phone = phone
    profile.email = email
    profile.place=place
    profile.post=post
    profile.pin=pin

    profile.save()
    return HttpResponse('''<script>alert("Registration Successfull"); window.location='/';</script>''')



def dregister(request):
    ob=VehicleType.objects.all()
    return render(request,"DRIVER/dregister.html",{'vtype':ob})

def dregister_post(request):
    name=request.POST['name']
    phone=request.POST['phone']
    email = request.POST['email']
    vnum = request.POST['vnum']
    vtype=request.POST['vtype']
    lphoto=request.FILES['image1']
    rphoto=request.FILES['image2']
    iphoto=request.FILES['image3']
    vphoto=request.FILES['image4']

    if Driver.objects.filter(vehnum=vnum).exists():
        return HttpResponse('''<script>alert("Number already exists"); window.location='/dregister';</script>''')

    password = request.POST['password']

    fs = FileSystemStorage()
    fs1 = fs.save(lphoto.name, lphoto)

    ft = FileSystemStorage()
    ft1 = ft.save(rphoto.name, rphoto)

    fu = FileSystemStorage()
    fu1 = fu.save(iphoto.name, iphoto)

    fv = FileSystemStorage()
    fv1 = fv.save(vphoto.name, vphoto)


    login_details = Login_table()
    login_details.username = email
    login_details.password = password
    login_details.type = 'pending'
    login_details.save()

    profile = Driver()
    profile.LOGIN = login_details
    profile.name = name
    profile.phone = phone
    profile.email = email
    profile.vehnum=vnum
    profile.VTYPE_id=vtype
    # profile.VTYPE=VehicleType.objects.get(id=vtype)
    profile.licencep = fs1
    profile.registrationp = ft1
    profile.insurancep = fu1
    profile.vehiclep = fv1
    profile.save()
    return HttpResponse('''<script>alert("Registration Successfull"); window.location='/';</script>''')



@login_required(login_url='/')
def Adminhome(request):
    # Retrieve all trips
    trips = Trip.objects.all()

    # Count trips per driver
    driver_trip_count = trips.values('DRIVER__name').annotate(trip_count=models.Count('id'))

    # Prepare data for the chart
    driver_names = [entry['DRIVER__name'] for entry in driver_trip_count]
    trip_counts = [entry['trip_count'] for entry in driver_trip_count]

    return render(request, "ADMIN/ahome.html", {
        'driver_names': driver_names,
        'trip_counts': trip_counts,
    })
@login_required(login_url='/')
def Managevtype(request):
    ob=VehicleType.objects.all()
    return render(request, "ADMIN/managevtype.html", {"vtype":ob})
@login_required(login_url='/')
def Add_vtype(request):
    return render(request, "ADMIN/addvtype.html")
@login_required(login_url='/')
def insert_vtype(request):
    type=request.POST['textfield']
    seats=request.POST['textfield2']
    price=request.POST['price']
    ob=VehicleType()
    ob.type=type
    ob.price=price
    ob.seats=seats
    ob.save()
    return HttpResponse('''<script>alert('Inserted');window.location='/Managevtype'</script>''')

@login_required(login_url='/')
def vtype_delete(request,id):
    a=VehicleType.objects.get(id=id)
    a.delete()
    return HttpResponse('''<script>alert('deleted');window.location='/Managevtype'</script> ''')

@login_required(login_url='/')
def Edit_vtype(request, id):
    request.session['lid']=id
    ob=VehicleType.objects.get(id=id)
    return render(request,"ADMIN/editvtype.html" ,{'data':ob})
@login_required(login_url='/')
def Edit_vtype_add(request):
    type=request.POST['textfield']
    seats=request.POST['textfield2']
    price=request.POST['price']
    ob=VehicleType.objects.get(id=request.session['lid'])
    ob.type=type
    ob.price=price
    ob.seats=seats
    ob.save()
    return HttpResponse('''<script>alert("Edited Successfully");window.location='/Managevtype'</script>''')


@login_required(login_url='/')
def Verify_driver(request):
    ob=Driver.objects.all().order_by('-id')
    return render(request, "ADMIN/verifydriver.html",{'data':ob})
@login_required(login_url='/')
def admin_view_more_drivers(request,id):
    ob=Driver.objects.get(id=id)
    return render(request, 'ADMIN/view_more_drivers.html',{'ob':ob})
#-------------------------------------------------------------------------------------------------------------


# @login_required(login_url='/')
# def accept_driver(request,id):
#     ob=Login_table.objects.get(id=id)
#     ob.type='driver'
#     ob.save()
#     return HttpResponse('''<script>alert("Driver Accepted");window.location='/Verify_driver'</script>''')

# @login_required(login_url='/')
# def unblock_driver(request, id):
#     ob = Login_table.objects.get(id=id)
#     ob.type = 'driver'  # Unblock the user, set type back to 'user'
#     ob.save()
#     return HttpResponse('''<script>alert("Driver Unblocked");window.location='/Verify_driver'</script>''')
# @login_required(login_url='/')
# def reject_driver(request, id):
#     login_driver = Login_table.objects.get(id=id)
#     if Driver.objects.filter(LOGIN=login_driver).exists():
#         user_entry = Driver.objects.get(LOGIN=login_driver)
#         user_entry.delete()
#         login_driver.delete()

#     return HttpResponse('''<script>alert("User Rejected and Removed");window.location='/Verify_driver'</script>''')


from django.core.mail import send_mail
from django.conf import settings

@login_required(login_url='/')
def accept_driver(request, id):
    ob = Login_table.objects.get(id=id)
    ob.type = 'driver'
    ob.save()
    
    # Send email notification
    message = 'From Taxi Fare - Your account has been accepted as a driver.'
    try:
        send_mail(
            'ACCOUNT ACCEPTED',
            message,
            settings.EMAIL_HOST_USER,
            [ob.username, ],
            fail_silently=False
        )
    except Exception as e:
        print(e)
    
    return HttpResponse('''<script>alert("Driver Accepted");window.location='/Verify_driver'</script>''')

@login_required(login_url='/')
def unblock_driver(request, id):
    ob = Login_table.objects.get(id=id)
    ob.type = 'driver'  # Unblock the user, set type back to 'driver'
    ob.save()
    
    # Send email notification
    message = 'From Taxi Fare - Your account has been unblocked. You can now log in.'
    try:
        send_mail(
            'ACCOUNT UNBLOCKED',
            message,
            settings.EMAIL_HOST_USER,
            [ob.username, ],
            fail_silently=False
        )
    except Exception as e:
        print(e)
    
    return HttpResponse('''<script>alert("Driver Unblocked");window.location='/Verify_driver'</script>''')

@login_required(login_url='/')
def reject_driver(request, id):
    login_driver = Login_table.objects.get(id=id)
    
    if Driver.objects.filter(LOGIN=login_driver).exists():
        user_entry = Driver.objects.get(LOGIN=login_driver)
        user_entry.delete()
    
    # Send email notification
    message = 'From Taxi Fare - Your account has been rejected and removed.'
    try:
        send_mail(
            'ACCOUNT REJECTED',
            message,
            settings.EMAIL_HOST_USER,
            [login_driver.username, ],
            fail_silently=False
        )
    except Exception as e:
        print(e)

    login_driver.delete()
    return HttpResponse('''<script>alert("User Rejected and Removed");window.location='/Verify_driver'</script>''')


@login_required(login_url='/')
def generate_qr(request, id):
    driver = Driver.objects.get(id=id)

    # Collect the driver's information into a string
    driver_details = (driver.id
    )

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Controls the size of each "box" in the QR code grid
        border=4,  # Controls the border width
    )
    qr.add_data(driver_details)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)

    fs = FileSystemStorage()
    filename = f"driver_qr_{driver.id}.png"
    file_path = fs.save(filename, ContentFile(img_io.getvalue()))

    driver.qr = file_path
    driver.save()

    return HttpResponse('''<script>alert("QR generated Successfully");window.location='/Verify_driver'</script>''')
@login_required(login_url='/')
def view_rating(request):
    ob=Rating.objects.all().order_by('-id')
    return render(request,"ADMIN/viewrating.html", {'data':ob})
@login_required(login_url='/')
def view_registered_customer(request):
    query = request.GET.get('search', '')
    if query:
        data = Customer.objects.filter(name__icontains=query)  # Assuming you have a Customer model
    else:
        data = Customer.objects.all()
    return render(request, "ADMIN/regcus.html", {'data':data})


from django.db.models import Count

@login_required(login_url='/')
def Driverhome(request):
    driver = Driver.objects.get(LOGIN_id=request.session['lid'])
    trips = Trip.objects.filter(DRIVER_id=driver,payment='paid')

    total_trips = trips.count()

    trips_per_date = trips.values('date').annotate(count=Count('id')).order_by('date')

    labels = [trip['date'].strftime('%Y-%m-%d') for trip in trips_per_date]
    data = [trip['count'] for trip in trips_per_date]

    return render(request, "DRIVER/dhome.html", {
        'total_trips': total_trips,
        'chart_labels': labels,
        'chart_data': data,
    })

@login_required(login_url='/')
def driver_view_feedbacks(request):
    driver = Driver.objects.get(LOGIN_id=request.session['lid'])
    trips = Trip.objects.filter(DRIVER_id=driver)
    ratings = Rating.objects.filter(TRIP__id__in=trips).order_by('-id')
    return render(request, 'DRIVER/ratings.html',{'data':ratings})

@login_required(login_url='/')
def driver_profile(request):
    my_profile = Driver.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'DRIVER/my_profile.html',{'driver':my_profile})
@login_required(login_url='/')
def edit_profile(request,id):
    profile = Driver.objects.get(id=id)
    vtype = VehicleType.objects.all()
    if request.method == 'POST':
        profile.name=request.POST['name']
        profile.email=request.POST['email']
        profile.phone=request.POST['phone']

        vtype_id = request.POST['vtype']
        profile.VTYPE = VehicleType.objects.get(id=vtype_id)

        if 'licencep' in request.FILES:
            profile.licencep = request.FILES['licencep']
        if 'registrationp' in request.FILES:
            profile.registrationp = request.FILES['registrationp']

        if 'insurancep' in request.FILES:
            profile.insurancep = request.FILES['insurancep']

        if 'vehiclep' in request.FILES:
            profile.vehiclep = request.FILES['vehiclep']

        profile.save()

        return HttpResponse('''<script>alert("Profile Edited Successfully");window.location='/driver_profile'</script>''')
    return render(request, 'DRIVER/edit_profile.html', {'profile': profile, 'vtype': vtype})

@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        old = request.POST['old']
        new = request.POST['new']
        confirm = request.POST['confirm']

        driver = Login_table.objects.get(id=request.session['lid'])
        if driver.password == old:
            if new == confirm:
                driver.password = confirm
                driver.save()
                return HttpResponse('''<script>alert("Password changed successfully!");window.location='/driver_profile';</script>''')
            else:
                return HttpResponse('''<script>alert("New Password and Confirm Password do not match");window.location='/change_password';</script>''')
        return HttpResponse('''<script>alert("Old Password is incorrect");window.location='/change_password';</script>''')
    return render(request, 'DRIVER/change_password.html')

@login_required(login_url='/')
def driver_view_users(request):
    ob=Customer.objects.all()
    print(ob)
    return render(request,"DRIVER/view_users.html", {'data':ob})
@login_required(login_url='/')
def searchuser(request):
    s=request.POST['s']
    ob=Customer.objects.filter(name__istartswith=s)
    return render(request,"DRIVER/view_users.html", {'data':ob,"s":s})


@login_required(login_url='/')
def start_ride(request):
   

    ob=Trip.objects.filter(DRIVER__LOGIN__id=request.session['lid'],end='pending')
    if len(ob)==0:
        return render(request,"DRIVER/map_start.html")
    else:
        request.session['tid']=ob[0].id
        return render(request,"DRIVER/map_stop.html")

@login_required(login_url='/')
def add2(request,id):
    request.session['tid']=id
    return render(request,"DRIVER/map_stop.html")
@login_required(login_url='/')
def add1(request):
   
    lat=request.POST['lat']
    lon=request.POST['lon']
    ps=request.POST['pl']

    ob=Trip()
    ob.DRIVER=Driver.objects.get(LOGIN__id=request.session['lid'])
    ob.start=lat+","+lon
    ob.end='pending'
    ob.splace=ps
    ob.date=datetime.today()
    ob.distance="pending"
    ob.save()
    return redirect("/start_ride")


import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0077

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance
@login_required(login_url='/')
def add3(request):
    tid=request.session['tid']
    lat=request.POST['lat']
    pl=request.POST['pl']
    lon=request.POST['lon']
    ob = Trip.objects.get(id=tid)
    lat1,lon1=ob.start.split(",")
    rate = ob.DRIVER.VTYPE.price
    ob.eplace=pl
    print(lat,lon,lat1,lon1)
    d=haversine(float(lat),float(lon),float(lat1),float(lon1))
    d=int(d)+20
    ob.end=lat+","+lon
    print('-------++++++++++--------',d)

    ob.distance=d
    ob.price=int(d)*rate
    ob.save()
    return redirect("/view_trip_history")
@login_required(login_url='/')
def view_trip_history(request):
    ob=Trip.objects.filter(DRIVER__LOGIN_id=request.session['lid']).order_by("-id")
    print(ob)
    return render(request,"DRIVER/triphistory.html", {'data':ob})

@login_required(login_url='/')
def generate_bill(request, id):
    trip = Trip.objects.get(id=id)
    distance = float(trip.distance)
    rate_per_km = trip.DRIVER.VTYPE.price
    total_amount = distance * rate_per_km

    start_lat = trip.start  # Ensure you have these fields populated
    end_lat = trip.end

    start_location_link = f"https://www.google.com/maps/@{start_lat},{start_lat},15z"
    end_location_link = f"https://www.google.com/maps/@{end_lat},{end_lat},15z"

    # Prepare QR code data
    qr_data = f"""
        BILL NUMBER : {trip.id}
        Distance : {trip.distance}
        Starting Location: <a href="{start_location_link}">Click here</a>
        Ending Location: <a href="{end_location_link}">Click here</a>
        Total Amount: {total_amount} INR
        """

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Save the image to a BytesIO buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Define the filename for the QR code image
    filename = f"trip_{trip.id}_qr_code.png"

    # Save the QR code image to the Trip model's bill field
    trip.bill.save(filename, ContentFile(buffer.getvalue()), save=True)
    return HttpResponse('''<script>alert("Bill Generated Successfully");window.location='/view_trip_history'</script>''')

@login_required(login_url='/')
def view_rating1(request):
    ob=Rating.objects.filter(TRIP__DRIVER__LOGIN_id=request.session['lid'])
    return render(request,"DRIVER/rating1.html",{'data':ob})

@login_required(login_url='/')
def Customerhome(request):
    ratings = Rating.objects.exclude(TRIP__CUSTOMER__LOGIN_id=request.session['lid'])
    return render(request, "CUSTOMER/chome.html",{'ratings':ratings})

@login_required(login_url='/')
def view_profile(request):
    customer = Customer.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'CUSTOMER/view_profile.html',{'customer':customer})
@login_required(login_url='/')
def customer_edit_profile(request,id):
    customer = Customer.objects.get(id=id)
    if request.method == 'POST':
        customer.name=request.POST['name']
        customer.phone=request.POST['phone']
        customer.email=request.POST['email']
        customer.place=request.POST['place']
        customer.post=request.POST['post']
        customer.pin=request.POST['pin']
        customer.save()
        return HttpResponse('''<script>alert("Profile Edited Successfully");window.location='/view_profile'</script>''')
    return render(request, 'CUSTOMER/edit_profile.html',{'customer':customer})

@login_required(login_url='/')
def viewdriver(request):

    return render(request, 'CUSTOMER/viewdriver.html')


# def view_trip_history1(request):
#     ob=Trip.objects.filter(CUSTOMER__LOGIN_id=request.session['lid'])
#     return render(request, "CUSTOMER/triphistorycust.html",{'data':ob})
@login_required(login_url='/')
def view_trip_history1(request):
    search_id = request.GET.get('search_id')


    trips = Trip.objects.filter(id=search_id)
    if search_id:
        trips = trips.filter(id=search_id)


    context = {'data': trips}
    return render(request, 'CUSTOMER/triphistorycust.html', context)
@login_required(login_url='/')
def user_pay_proceed(request,id,amt):
    request.session['rid'] = id
    request.session['pay_amount'] = amt
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    payment = client.order.create({'amount': str(amt).split(".")[0]+"00", 'currency': "INR", 'payment_capture': '1'})
    return render(request,'CUSTOMER/UserPayProceed.html',{'p':payment,'val':[],"lid":request.session['lid'],"id":request.session['rid']})

def on_payment_success(request):
    request.session['rid'] = request.GET['id']
    request.session['lid'] = request.GET['lid']
    ob1 = auth.authenticate(username="admin", password="admin")
    if ob1 is not None:
        auth.login(request, ob1)
    trip = Trip.objects.get(id=request.session['rid'])
    trip.payment='paid'
    trip.CUSTOMER=Customer.objects.get(LOGIN__id=request.session['lid'])
    trip.save()
    return HttpResponse('''<script>alert("Thank you for paying with Razor Pay");window.location='/view_trip_history2'</script>''')

@login_required(login_url='/')
def view_trip_history2(request):

    ob= Trip.objects.filter(CUSTOMER__LOGIN__id=request.session['lid'])


    context = {'data': ob}
    return render(request, 'CUSTOMER/triphistorycust1.html', context)
@login_required(login_url='/')
def add_rating(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        rating = request.POST.get('rating')
        review = request.POST.get('review')

        trip = Trip.objects.get(id=trip_id)

        rating_instance = Rating(
            TRIP=trip,  # Set the related trip
            rating=rating,  # Set the rating value
            review=review,  # Set the review text
            date=datetime.now()  # Use timezone for the date
        )
        rating_instance.save()
        return redirect('/view_trip_history1')
    return render(request, 'CUSTOMER/triphistorycust.html')



@login_required(login_url='/')
def view_drivers(request):
    drivers = Driver.objects.filter(LOGIN__type='driver')
    return render(request, 'CUSTOMER/view_drivers.html',{'drivers':drivers})

@login_required(login_url='/')
def view_drivers_view_more(request,id):
    drivers = Driver.objects.get(id=id)
    return render(request, 'CUSTOMER/view_more_driver.html',{'drivers':drivers})

@login_required(login_url='/')
def block_driver(request, id):
    ob = Login_table.objects.get(id=id)
    message = 'From Taxi Fare -  Hey user,  Your Account is blocked, Contact the admin'
    try:
        send_mail(
            'ACCOUNT IS BLOCKED',
            message,
            settings.EMAIL_HOST_USER,
            [ob.username, ],
            fail_silently=False
        )
    except Exception as e:
        print(e)
    ob.type = 'blocked'
    ob.save()
    return HttpResponse('''<script>alert("User Blocked");window.location='/Verify_driver'</script>''')

from django.http import JsonResponse
import json
def fetch_driver_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            vehicle_number = data.get('vehicle_number')

            # Check if vehicle number is provided
            if vehicle_number:
                driver = Driver.objects.get(id=vehicle_number)
                ob=Rating.objects.filter(TRIP__DRIVER__id=driver.id)
                ar=0
                for i in ob:
                    ar+=i.rating
                if len(ob)>0:
                    ar=ar/len(ob)
                s=False
                if len(ob)>0:
                    s=True
                # Return driver details in the response

                # LOGIN = models.ForeignKey(Login_table, on_delete=models.CASCADE)
                # VTYPE = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
                # name = models.CharField(max_length=100)
                # vehnum = models.CharField(max_length=100)
                # email = models.CharField(max_length=100)
                # phone = models.BigIntegerField()
                # licencep = models.FileField()
                # registrationp = models.FileField()
                # insurancep = models.FileField()
                # vehiclep = models.FileField()
                # qr = models.Fil


                return JsonResponse({
                    'success': True,
                    'driver': {
                        'name': driver.name,
                        'email': driver.email,
                        'mobile_number': driver.phone,
                        'vehicle_number': driver.vehnum,
                        'vehicle_type': driver.VTYPE.type,
                        's': s,
                        "ar":ar
                    }
                })
            else:
                return JsonResponse({'success': False, 'error': 'Vehicle number is required.'})
        except :
            try:
                vehicle_number = data.get('vehicle_number')

                # Check if vehicle number is provided
                if vehicle_number:
                    driver = Driver.objects.get(vehnum=vehicle_number)

                    # Return driver details in the response

                    # LOGIN = models.ForeignKey(Login_table, on_delete=models.CASCADE)
                    # VTYPE = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
                    # name = models.CharField(max_length=100)
                    # vehnum = models.CharField(max_length=100)
                    # email = models.CharField(max_length=100)
                    # phone = models.BigIntegerField()
                    # licencep = models.FileField()
                    # registrationp = models.FileField()
                    # insurancep = models.FileField()
                    # vehiclep = models.FileField()
                    # qr = models.Fil
                    ob = Rating.objects.filter(TRIP__DRIVER__id=driver.id)
                    ar = 0
                    for i in ob:
                        ar += i.rating
                    if len(ob) > 0:
                        ar = ar / len(ob)
                    s = False
                    if len(ob) > 0:
                        s = True

                    return JsonResponse({
                        'success': True,
                        'driver': {
                            'name': driver.name,
                            'email': driver.email,
                            'mobile_number': driver.phone,
                            'vehicle_number': driver.vehnum,
                            'vehicle_type': driver.VTYPE.type,
                            's': s,
                            "ar": ar
                        }
                    })
                else:
                    return JsonResponse({'success': False, 'error': 'Vehicle number is required.'})
            except:
                pass
            return JsonResponse({'success': False, 'error': 'Driver not found.'})

        return JsonResponse({'success': False, 'error': 'Invalid request method.'})
