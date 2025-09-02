from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout   # 👈 add authenticate + logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, DonationForm, BloodRequestForm
from .models import Donation, BloodRequest,Hospital
from .models import Profile
import math


# -------------------- landing Page --------------------
def landing(request):
    return render(request, "donation/index.html")


# -------------------- Home --------------------
@login_required
def home(request):
    return render(request, "donation/home.html")


# -------------------- Signup --------------------
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get("email")
            user.save()

            # Create profile
            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data.get("full_name"),
                mobile=form.cleaned_data.get("mobile"),
            )

            messages.success(request, "Account created successfully. Please login.")
            return redirect("login")
        else:
            messages.error(request, "Error creating account. Please check the form.")
    else:
        form = RegistrationForm()
    return render(request, "donation/register.html", {"form": form})


# -------------------- Login --------------------
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back {username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "donation/login.html", {"form": form})


# -------------------- Logout --------------------
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("index")


# -------------------- User History --------------------
@login_required
def history(request):
    donations = Donation.objects.filter(user=request.user).order_by("-donation_date")
    requests = BloodRequest.objects.filter(user=request.user).order_by("-date")
    return render(request, "donation/history.html", {"donations": donations, "requests": requests})


# -------------------- Live History --------------------
def live_history(request):
    donations = Donation.objects.select_related("user").order_by("-donation_date")[:20]
    requests = BloodRequest.objects.select_related("user").order_by("-date")[:20]
    return render(request, "donation/live_history.html", {"donations": donations, "requests": requests})

# -------------------- Donate Blood --------------------
@login_required
def donate_blood(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user

            lat = request.POST.get("latitude")
            lng = request.POST.get("longitude")

            if lat and lng:
                obj.latitude = float(lat)
                obj.longitude = float(lng)

                # find nearest hospital
                nearest = find_nearest_hospital(obj.latitude, obj.longitude)
            else:
                nearest = None

            obj.save()

            return render(request, "donation/donate_success.html", {
                "nearest_hospital": nearest,
                "donation": obj
            })
    else:
        form = DonationForm()
    return render(request, "donation/donate_blood.html", {"form": form})


# -------------------- Request Blood --------------------
@login_required
def request_blood(request):
    if request.method == "POST":
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user

            lat = request.POST.get("latitude")
            lng = request.POST.get("longitude")

            if lat and lng:
                obj.latitude = float(lat)
                obj.longitude = float(lng)

                # find nearest hospital
                nearest = find_nearest_hospital(obj.latitude, obj.longitude)
            else:
                nearest = None

            obj.save()

            return render(request, "donation/request_success.html", {
                "nearest_hospital": nearest,
                "blood_request": obj
            })
    else:
        form = BloodRequestForm()
    return render(request, "donation/request_blood.html", {"form": form})

# -------------------- Utility Functions --------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


def find_nearest_hospital(user_lat, user_lng):
    hospitals = Hospital.objects.all()
    nearest = None
    min_distance = float("inf")
    for hospital in hospitals:
        distance = haversine(user_lat, user_lng, hospital.latitude, hospital.longitude)
        if distance < min_distance:
            min_distance = distance
            nearest = hospital
    return nearest