from django.contrib.auth.models import AbstractUser, Group, User
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model


# User = get_user_model()

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Ensure the user is in only one group
        self.groups.clear()
        if self.is_doctor:
            group, created = Group.objects.get_or_create(name="Doctors")
            self.groups.add(group)
        elif self.is_receptionist:
            group, created = Group.objects.get_or_create(name="Receptionists")
            self.groups.add(group)
        else:
            group, created = Group.objects.get_or_create(name="Users")
            self.groups.add(group)
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')  # Link to the User model
    dob = models.DateField(null=True, blank=True)  # Date of Birth
    medical_history = models.TextField(null=True, blank=True)  # Medical history
    # Add other fields if needed

    def __str__(self):
        return f'{self.user.username} Profile'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    consultation_fees = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    availability = models.TextField()
    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20, default="Pending")
    confirmed = models.BooleanField(default=False)  # To mark the appointment as confirmed or not
    paid = models.BooleanField(default=False)  # To indicate if the payment was made
    # payment_status = models.BooleanField(default=False)
    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.appointment_date} by {self.user.username}"

class Receptionists(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='receptionist_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    hire_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)  # Replace with your Appointment model
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Store in dollars, not cents
    payment_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='Success')  # E.g., 'succeeded', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.user.username}"