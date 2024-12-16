from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WasteListing, Profile, Transaction
from django.middleware.csrf import get_token
from .forms import WasteListingForm, ProfileForm
from django.contrib.auth.models import User
import africastalking




def homepage(request):
    return render(request, 'homepage.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.GET.get('type')  # 'Producer' or 'Recycler'

        print(f"user_type from GET: {user_type}")  # Debugging statement

        if not username or not email or not password or not user_type:
            messages.error(request, "All fields are required.")
            return redirect('signup')

        # Validate user_type
        if user_type not in ['Producer', 'Recycler']:
            messages.error(request, "Invalid user type selected.")
            return redirect('signup')

        try:
            # Check if the user exists
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )

            # Set the password for new users
            if created:
                user.set_password(password)
                user.save()

            # Check if the profile exists
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'user_type': user_type,
                    'organization_name': "Default Organization",  # Replace with actual data
                    'location': "Default Location"  # Replace with actual data
                }
            )

            # If the profile already existed, update the user_type
            if not profile_created:
                profile.user_type = user_type
                profile.save()

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')

        except Exception as e:
            print(f"Error details: {e}")  # Debugging statement
            messages.error(request, f"Error creating account: {e}")
            return redirect('signup')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debugging: Print inputs
        print(f"Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                print(f"User type: {profile.user_type}")  # Debugging statement
                if profile.user_type == 'Producer':
                    return redirect('list_waste')
                elif profile.user_type == 'Recycler':
                    return redirect('browse_waste')
            except Profile.DoesNotExist:
                messages.error(request, 'Profile not found. Contact support.')
                return redirect('homepage')
        else:
            print("Authentication failed.")  # Debugging statement
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Profile will be created automatically by create_user_profile
        pass

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def view_profile(request):
    profile = request.user.profile
    return render(request, 'view_profile.html', {'profile': profile})


@login_required
def list_waste(request):
    if request.method == 'POST':
        form = WasteListingForm(request.POST)
        if form.is_valid():
            waste = form.save(commit=False)
            try:
                # Associate the producer with the logged-in user's profile
                waste.producer = request.user.profile
                waste.save()
                messages.success(request, "Waste listing created successfully.")
                return redirect('browse_waste')
            except Profile.DoesNotExist:
                messages.error(request, "Your profile is incomplete. Please contact support.")
                return redirect('edit_profile')
    else:
        form = WasteListingForm()
    return render(request, 'list_waste.html', {'form': form})


@login_required
def browse_waste(request):
    # Fetch all waste listings
    waste_listings = WasteListing.objects.all()
    
    # Pass the listings to the template
    return render(request, 'browse_waste.html', {'waste_listings': waste_listings})

@login_required
def claim_waste(request, waste_id):
    waste = get_object_or_404(WasteListing, id=waste_id)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Send SMS notification after claiming waste
        try:
            # Initialize Africa's Talking API
            africastalking.initialize(username="miabritacreation", api_key="atsk_3554501a42f3f1f1448d93ff830158014916064ff660ee2b98611960388b58db9103fb2d")
            
            # Send SMS
            sms = africastalking.SMS
            response = sms.send(
                message=f"You have successfully claimed waste: {waste.waste_type} at {waste.location}. Quantity: {waste.quantity} kg",
                recipients=["+" + str(phone_number)]
            )
            print("SMS Response:", response)  # For debugging
            
            # Show success message to the user
            messages.success(request, "Waste claimed successfully")
            
            # Link the waste to the recycler (assuming you have a profile or user model)
            recycler = request.user.profile  # Assuming the user has a profile model
            Transaction.objects.create(waste_listing=waste, recycler=recycler)
            
            # Redirect to the waste browse page
            return redirect('browse_waste')
        
        except Exception as e:
            # If sending SMS fails, show an error message
            messages.error(request, f"Error sending SMS: {e}")
    
    # If the request is not POST, redirect to browse_waste
    return redirect('browse_waste')