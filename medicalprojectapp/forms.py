from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Doctor, Appointment, UserProfile, Profile 

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_doctor', 'is_receptionist']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name']
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_doctor', 'is_receptionist')

class SignUpForm(CustomUserCreationForm):
    ROLE_CHOICES = [
        ('users', 'Users'),
        # ('doctors', 'Doctors'),
        ('receptionists', 'Receptionists'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Use password1 to set the user's password
        user.set_password(self.cleaned_data['password1'])  
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # Replace with your model if different
        fields = ['dob', 'medical_history'] 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'medical_history']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'consultation_fees', 'availability']

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name','specialization', 'availability', 'consultation_fees']
        widgets = {
            'availability': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter availability (e.g., Mon-Fri 9am-5pm)'}),
            'consultation_fees': forms.NumberInput(attrs={'placeholder': 'Enter consultation fee'}),
        }

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['availability']  # Only update availability

class ConsultationFeeForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['consultation_fees'] 

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['user', 'doctor', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }