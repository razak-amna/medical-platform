from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, SignUpForm, AvailabilityForm, ConsultationFeeForm, DoctorForm, AppointmentForm, EditProfileForm, ProfileForm, DoctorUpdateForm
from .models import User, Doctor, Appointment, UserProfile, Profile, Receptionists, Payment
from django.contrib.auth.models import Group
from django.http import Http404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request, 'base_generic.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            user = form.save()

            # Ensure the groups exist before adding the user
            role = form.cleaned_data['role']
            # if role == 'doctors':
            #     user.is_doctor = True
            #     doctor_group, created = Group.objects.get_or_create(name='Doctors')
            #     user.groups.add(doctor_group)
            #     user.save()
            #     Doctor.objects.get_or_create(user=user)  # Create the Doctor object
            #     Profile.objects.update_or_create(user=user, defaults={'is_doctor': True})
            if role == 'receptionists':
                user.is_receptionist = True
                receptionist_group, created = Group.objects.get_or_create(name='Receptionists')
                user.groups.add(receptionist_group)
                user.save()
                Receptionists.objects.get_or_create(user=user)  # Create the Receptionist object
                Profile.objects.update_or_create(user=user, defaults={'is_receptionist': True})
            else:
                # user.is_doctor = False
                user.is_receptionist = False
                user.groups.add(Group.objects.get(name='Users'))
                user.save()
                Profile.objects.update_or_create(user=user, defaults={'is_doctor': False, 'is_receptionist': False})

            # Log the user in automatically after successful signup
            login(request, user)

            # Redirect based on the user's role
            # if user.is_doctor:
            #     return redirect('doctor_profile')  # Redirect to doctor profile page
            if user.is_receptionist:
                return redirect('receptionist_profile')  # Redirect to receptionist profile page
            else:
                return redirect('user_profile')  # Redirect to normal user profile page
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect based on role
                # if user.is_doctor:
                #     return redirect('doctor_profile')  # Doctor profile page
                if user.is_receptionist:
                    return redirect('receptionist_profile')  # Receptionist profile page
                elif user.is_authenticated:
                    return redirect('user_profile')  # Regular user profile page
                else:
                    # If no role is assigned
                    return redirect('login')  # Or you can show a message saying that no role was found
            else:
                # Invalid credentials
                return redirect('login')  # Or you can show an error message
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return JsonResponse({'status': 'success', 'redirect_url': '/user_profile/'})
#         else:
#             return JsonResponse({'status': 'failure', 'message': 'Invalid username or password'})

#     # For GET requests, generate a new CSRF token
#     # csrf_token = get_token(request)
#     # return JsonResponse({'csrf_token': csrf_token})
#     # Return an error if the request is not POST
#     return JsonResponse({'status': 'failure', 'message': 'Invalid request method'}, status=405)

def profile(request):
    user = request.user
    if user.is_authenticated:
        if hasattr(user, 'profile') and user.profile.is_doctor:
            return redirect('doctor_profile')
        elif hasattr(user, 'profile') and user.profile.is_receptionist:
            return redirect('receptionist_profile')
        else:
            return redirect('profile')
    else:
        return redirect('login')
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 # If the request is AJAX, return a JsonResponse
#                 if request.is_ajax():
#                     return JsonResponse({'status': 'success', 'redirect_url': get_redirect_url(user)})

#                 # If not AJAX, redirect as usual
#                 if user.is_doctor:
#                     return redirect('doctor_profile')  # Replace with your specific doctor profile page
#                 elif user.is_receptionist:
#                     return redirect('receptionist_profile')  # Replace with your specific receptionist profile page
#                 else:
#                     # Redirect normal users to their profile
#                     return redirect('user_profile')  # Replace with your normal user profile page
#             else:
#                 # Invalid login credentials
#                 return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)

#     else:
#         form = AuthenticationForm()

#     return render(request, 'registration/login.html', {'form': form})

# def get_redirect_url(user):
#     """ Helper function to return the URL based on user role """
#     if user.is_doctor:
#         return 'doctor_profile'
#     elif user.is_receptionist:
#         return 'receptionist_profile'
#     else:
#         return 'user_profile'

@login_required
def user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(user=user)
    doctors = Doctor.objects.all()

    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            # Save the appointment for the user
            appointment = appointment_form.save(commit=False)
            appointment.user = user
            appointment.save()
            return redirect('user_profile')  # Redirect after successful appointment booking
    else:
        appointment_form = AppointmentForm()

    return render(request, 'registration/user_profile.html', {
        'appointments': appointments,
        'doctors': doctors,
        'appointment_form': appointment_form,
        'profile': profile  # Pass the profile information to the template
    })

# @login_required
# def edit_profile(request):
#     # user_profile = user.userprofile  # Assuming each user has a UserProfile
#     # Get the user's profile
#     # user_profile = request.user.profile
#     profile = Profile.objects.get(user=request.user)
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             return redirect('user_profile')  # Redirect back to the user profile after saving
#     else:
#         form = EditProfileForm(instance=user_profile)

#     return render(request, 'registration/edit_profile.html', {'form': form})
@login_required
def edit_profile(request):
    # Try to get the profile for the logged-in user
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None  # Handle case where no profile exists
    
    # Handle form submission
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Redirect to user profile after saving
    else:
        form = ProfileForm(instance=profile)  # Pre-fill form with current profile data
    
    return render(request, 'registration/edit_profile.html', {'form': form})

@login_required
def doctor_profile(request):
    try:
        doctor = Doctor.objects.get(user=request.user)  # Fetch doctor profile for logged-in user
    except Doctor.DoesNotExist:
        # If the doctor profile doesn't exist, show an error message and redirect
        messages.error(request, 'Doctor profile not found. Please contact the admin to set up your profile.')
        return redirect('home')  # You can change this to any appropriate page, like the homepage

    appointments = Appointment.objects.filter(doctor=doctor)

    if request.method == 'POST':
        # Handle availability and consultation fee updates
        availability_form = AvailabilityForm(request.POST, instance=doctor)
        consultation_form = ConsultationFeeForm(request.POST, instance=doctor)

        if availability_form.is_valid():
            availability_form.save()
            messages.success(request, 'Availability updated successfully!')
        
        if consultation_form.is_valid():
            consultation_form.save()
            messages.success(request, 'Consultation fee updated successfully!')

        return redirect('doctor_profile')  # Redirect after saving changes
    else:
        availability_form = AvailabilityForm(instance=doctor)
        consultation_form = ConsultationFeeForm(instance=doctor)

    return render(request, 'registration/doctor_profile.html', {
        'doctor': doctor,
        'appointments': appointments,
        'availability_form': availability_form,
        'consultation_form': consultation_form
    })

@login_required
def receptionist_profile(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST)
        if doctor_form.is_valid():
            doctor_form.save()
            return redirect('receptionist_profile')
    else:
        doctor_form = DoctorForm()

    return render(request, 'registration/receptionist_profile.html', {
        'doctors': doctors,
        'doctor_form': doctor_form
    })

# Notify user upon appointment confirmation
def notify_user_of_appointment(appointment):
    # Logic to notify users (e.g., email or message)
    user = appointment.user
    message = f"Your appointment with {appointment.doctor.name} on {appointment.appointment_date} has been confirmed."
    user.email_user("Appointment Confirmation", message)  # Example notification method


@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            # Notify the user about their appointment
            notify_user_of_appointment(appointment)

            return redirect('receptionist_profile')  # Redirect to receptionist profile
    else:
        form = AppointmentForm()
    return render(request, 'registration/create_appointment.html', {'form': form})

@login_required
def book_appointment(request):
    doctors = Doctor.objects.all()  # Fetch all doctors
    
    if request.method == 'POST':
        # Create appointment based on form data
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # Associate the appointment with the current user
            appointment.save()
            return redirect('payment_page')  # Redirect to payment page after booking appointment

    else:
        form = AppointmentForm()

    return render(request, 'registration/book_appointment.html', {
        'doctors': doctors,
        'form': form,
    })

import logging

logger = logging.getLogger(__name__)

# @csrf_exempt
# @login_required
# def payment_page(request):
#     if request.method == 'POST':
#         try:
#             amount = 1000  # Example amount in cents

#             # Create a PaymentIntent
#             intent = stripe.PaymentIntent.create(
#                 amount=amount,
#                 currency="usd",
#                 payment_method_types=["card"],
#             )
#             logger.debug(f"PaymentIntent created: {intent}")

#             # Get the appointment object (assuming it's passed in the request)
#             appointments = Appointment.objects.filter(user=request.user, confirmed=False)
#             if appointments.count() > 1:
#                 return render(request, 'registration/select_appointment.html', {
#                     'appointments': appointments,
#                     'amount': amount / 100,  # Send the amount in dollars
#                     'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
#                     'client_secret': intent.client_secret,
#                 })
#             elif appointments.count() == 1:
#                 appointment = appointments.first()
#             else:
#                 # Handle case when there are no unconfirmed appointments
#                 raise ValueError("No unconfirmed appointment found.")
#             logger.debug(f"Appointment found: {appointment}")

#             Payment.objects.create(
#                 user=request.user,
#                 appointment=appointment,
#                 amount=amount / 100,  # Store the amount in dollars
#                 payment_id=intent['id'],  # Save the PaymentIntent ID
#                 status='initiated',
#             )
#             logger.debug(f"Payment record created for user {request.user}")

#             return JsonResponse({
#                 'client_secret': intent.client_secret,
#                 'amount': amount / 100,  # Send the amount in dollars for frontend
#             })
#         except Exception as e:
#             logger.error(f"Error processing payment: {str(e)}")
#             messages.error(request, f"Error processing payment: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=500)

#     # If GET request, render payment page
#     stripe_publishable_key = "pk_test_51QgkLaJRBuLWMxDkyGLglxf0smlOLZSqg6fgcp7GX0z87APxFWmvbDCfrfdeaZAXWAA2Jb9NgkcbYiCdfMjJjprj00ira9ylrA"
#     return render(request, 'registration/payment_page.html', {
#         'stripe_publishable_key': stripe_publishable_key,
#         'client_secret': intent.client_secret,
#         'consultation_fees': amount / 100,  # Ensure amount in dollars
#     })
# @csrf_exempt
# @login_required
# def payment_page(request):
#     stripe_publishable_key = "pk_test_51QgkLaJRBuLWMxDkyGLglxf0smlOLZSqg6fgcp7GX0z87APxFWmvbDCfrfdeaZAXWAA2Jb9NgkcbYiCdfMjJjprj00ira9ylrA"

#     if request.method == 'POST':
#         try:
#             amount = 1000  # Example amount in cents

#             # Create a PaymentIntent
#             intent = stripe.PaymentIntent.create(
#                 amount=amount,
#                 currency="usd",
#                 payment_method_types=["card"],
#             )
#             logger.debug(f"PaymentIntent created: {intent}")

#             # Get the appointment object
#             appointments = Appointment.objects.filter(user=request.user, confirmed=False)
#             if appointments.count() > 1:
#                 return render(request, 'registration/select_appointment.html', {
#                     'appointments': appointments,
#                     'amount': amount / 100,  # Send the amount in dollars
#                     'stripe_publishable_key': stripe_publishable_key,
#                     'client_secret': intent.client_secret,
#                 })
#             elif appointments.count() == 1:
#                 appointment = appointments.first()
#             else:
#                 # Handle case when there are no unconfirmed appointments
#                 raise ValueError("No unconfirmed appointment found.")
#             logger.debug(f"Appointment found: {appointment}")

#             # Save payment details
#             Payment.objects.create(
#                 user=request.user,
#                 appointment=appointment,
#                 amount=amount / 100,  # Store the amount in dollars
#                 payment_id=intent['id'],  # Save the PaymentIntent ID
#                 status='initiated',
#             )
#             logger.debug(f"Payment record created for user {request.user}")
#             logger.debug(f"Client secret created: {intent.client_secret}")
#             return JsonResponse({
#                 'client_secret': intent.client_secret,
#                 'amount': amount / 100,  # Send the amount in dollars for frontend
#             })
#         except Exception as e:
#             logger.error(f"Error processing payment: {str(e)}")
#             messages.error(request, f"Error processing payment: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=500)

#     # Handle GET request
#     return render(request, 'registration/payment_page.html', {
#         'stripe_publishable_key': stripe_publishable_key,
#         'client_secret': '',  # For GET request, there might not be a client_secret yet
#         'consultation_fees': 10.00,  # Example fee, adjust as needed
#     })

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@login_required
def payment_page(request):
    if request.method == 'POST':
        try:
            amount = 1000  # Example amount in cents
            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                payment_method_types=["card"],
            )
            logger.debug(f"PaymentIntent created: {intent['id']} with client_secret: {intent.client_secret}")

            # Create a Payment record in the database
            appointment = Appointment.objects.filter(user=request.user, confirmed=False).first()
            if not appointment:
                raise ValueError("No unconfirmed appointment found for this user.")

            payment = Payment.objects.create(
                user=request.user,
                appointment=appointment,
                amount=amount / 100,  # Convert to dollars
                payment_id=intent['id'],
                status='initiated',
            )
            logger.debug(f"Payment record created for user {request.user}")

            return JsonResponse({
                'client_secret': intent.client_secret,
                'amount': amount / 100,  # Send the amount in dollars
            })
        except Exception as e:
            logger.error(f"Error creating PaymentIntent: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    # For GET requests, render the payment page
    return render(request, 'registration/payment_page.html', {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })
@csrf_exempt
def confirm_payment(request):
    """
    Handles the confirmation of payment after Stripe client-side confirmation.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Expecting JSON payload
            payment_id = data.get('payment_id')

            if not payment_id:
                raise ValueError("Missing payment_id in request data.")

            # Retrieve payment record in the database
            payment = Payment.objects.get(payment_id=payment_id)

            # Retrieve the PaymentIntent status from Stripe
            intent = stripe.PaymentIntent.retrieve(payment_id)

            if intent['status'] == 'succeeded':
                # Update payment status and related appointment
                payment.status = 'paid'
                payment.save()

                # Confirm the appointment
                payment.appointment.confirmed = True
                payment.appointment.save()

                logger.info(f"Payment {payment_id} succeeded for user {request.user}.")
                return JsonResponse({'message': 'Payment succeeded'})
            else:
                logger.warning(f"Payment {payment_id} failed or is incomplete.")
                return JsonResponse({'message': 'Payment not successful'}, status=400)
        except Exception as e:
            logger.error(f"Error confirming payment: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
#         )
#     except ValueError as e:
#         # Invalid payload
#         return JsonResponse({'error': 'Invalid payload'}, status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return JsonResponse({'error': 'Invalid signature'}, status=400)

#     # Handle the event
#     if event['type'] == 'payment_intent.succeeded':
#         intent = event['data']['object']
#         payment_id = intent['id']

#         # Update the Payment record in the database
#         try:
#             payment = Payment.objects.get(payment_id=payment_id)
#             payment.status = 'succeeded'
#             payment.save()

#             # Optionally, mark the appointment as confirmed
#             appointment = payment.appointment
#             appointment.confirmed = True
#             appointment.save()

#         except Payment.DoesNotExist:
#             return JsonResponse({'error': 'Payment record not found'}, status=404)

#     return JsonResponse({'status': 'success'}, status=200)


@login_required
def update_appointment(request, appointment_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            appointment = Appointment.objects.get(id=appointment_id, user=request.user)

            if data.get('status') == 'confirmed':
                appointment.confirmed = True  # Mark the appointment as confirmed
            if data.get('paid'):
                appointment.paid = True  # Mark the appointment as paid

            appointment.save()

            return JsonResponse({"status": "success"})
        except Appointment.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Appointment not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def is_receptionist(user):
    return user.groups.filter(name='Receptionists').exists()


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'registration/doctor_list.html', {'doctors': doctors})

@login_required
def update_doctor(request, doctor_id):
    if not is_receptionist(request.user):
        return redirect('no_access')  # Redirect to an access-denied page or home

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        form = DoctorUpdateForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorUpdateForm(instance=doctor)

    return render(request, 'registration/update_doctor.html', {'form': form, 'doctor': doctor})


PREDEFINED_RESPONSES = {
    "hello": "Namaste! How can I assist you with Ayurvedic guidance today?",
    "appointment": "You can schedule an appointment with our Ayurvedic specialist through the appointment page.",
    "help": "I am here to provide Ayurvedic guidance. Please share your query.",
    "doctor": "Our experienced Ayurvedic doctors are available for consultations. Visit the Doctors page to learn more.",
    "bye": "Goodbye! Stay healthy and take care.",
    "thankyou": "You're welcome! Feel free to reach out anytime for Ayurvedic advice.",
    "headache": "For headaches, try applying a paste of sandalwood or using lavender oil for relaxation. If it continues, consult a doctor.",
    "bodypain": "Consider an Ayurvedic massage with warm sesame oil or turmeric milk for relief from body pain.",
    "insomnia": "For better sleep, drink warm milk with a pinch of nutmeg before bedtime and avoid screen time in the evening.",
    "digestion": "For digestive issues, you can try sipping warm water with ginger and lemon or chewing fennel seeds after meals.",
    "stress": "Practice deep breathing or meditation, and consider Ashwagandha supplements for stress relief. Consult a doctor for proper dosage.",
    "cold": "For a cold, you can drink warm tulsi (holy basil) tea with honey and ginger. Steam inhalation may also help.",
    "skin": "For healthy skin, try applying aloe vera gel and drinking neem juice daily.",
    "hairfall": "To reduce hair fall, massage your scalp with coconut oil mixed with a few drops of rosemary oil. Amla juice is also beneficial.",
    "detox": "To detoxify, you can start your day with warm water and lemon, and include Triphala powder in your routine.",
    "immunity": "Boost your immunity by consuming chyawanprash daily and adding turmeric and black pepper to your meals.",
    "fever": "For mild fever, drink coriander seed tea or tulsi tea. If the fever persists, consult a doctor immediately.",
    "jointpain": "For joint pain, try applying warm mustard oil mixed with a pinch of turmeric or consuming fenugreek seeds daily."
}

def get_bot_response(user_message):
    # Check for the user message in the predefined responses
    for keyword, response in PREDEFINED_RESPONSES.items():
        if keyword.lower() in user_message.lower():
            return response
    # Default response if no keyword matches
    return "I'm sorry, I didn't understand that. Could you please clarify?"

# @csrf_exempt
# def chatbot(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_message = data.get('message')

#             if not user_message:
#                 return HttpResponseBadRequest("Message cannot be empty.")

#             if not request.user.is_authenticated:
#                 return JsonResponse({'error': 'User not authenticated'}, status=401)

#             user = request.user
#             chat_session, created = ChatSession.objects.get_or_create(user=user)

#             bot_response = get_bot_response(user_message)

#             # Create a new Chat object
#             chat = Chat.objects.create(
#                 user=user,
#                 chat_session=chat_session,
#                 user_message=user_message,
#                 bot_response=bot_response,
#                 timestamp=timezone.now(),
#             )

#             # Return the bot response as JSON
#             return JsonResponse({'message': bot_response})

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)

#     elif request.method == 'GET':
#         # Render the chatbot interface (optional)
#         return render(request, 'registration/chatbot.html')

#     return JsonResponse({'error': 'Method not allowed'}, status=405)
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        bot_response = get_bot_response(user_message)

        print(f"Received message: {user_message}")
        print(f"Bot response: {bot_response}")  # Add this line for debugging
        
        return JsonResponse({'user_message': user_message, 'bot_response': bot_response})

    return render(request, 'registration/chatbot.html')
