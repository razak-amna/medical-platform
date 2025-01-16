from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Doctor, Appointment, UserProfile, Profile, Payment
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','dob', 'medical_history')

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extend the UserAdmin
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Re-register the UserAdmin

# admin.site.register(User, CustomUserAdmin)
# admin.site.register(User)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_doctor', 'is_receptionist')

    # def clean_unique_name(self):
    #     # Allow unique_name only for doctors and receptionists
    #     if self.instance.is_doctor or self.instance.is_receptionist:
    #         if not self.instance.unique_name:
    #             raise forms.ValidationError("Unique name is required for doctors and receptionists.")
    #         if User.objects.filter(unique_name=self.instance.unique_name).exists():
    #             raise forms.ValidationError("This unique name is already taken.")
    #     return self.instance.unique_name


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'is_doctor', 'is_receptionist')



class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm  # Use the form that handles passwords
    form = CustomUserChangeForm  # Use the form for updating user details

    list_display = ('username', 'email', 'is_doctor', 'is_receptionist')
    list_filter = ('is_doctor', 'is_receptionist')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_doctor', 'is_receptionist')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2', 'is_doctor', 'is_receptionist')
        }),
    )
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_doctor and not Doctor.objects.filter(user=obj).exists():
            Doctor.objects.create(user=obj)



    # def save_model(self, request, obj, form, change):
    #     # Check if user is a doctor or receptionist and validate unique_name
    #     if obj.is_doctor or obj.is_receptionist:
    #         # Ensure unique_name is required only for doctor or receptionist
    #         if not obj.unique_name:
    #             raise forms.ValidationError("Unique name is required for doctors and receptionists.")
    #         # Ensure the unique name is not already taken
    #         if User.objects.filter(unique_name=obj.unique_name).exclude(id=obj.id).exists():
    #             raise forms.ValidationError("This unique name is already taken.")
    #     super().save_model(request, obj, form, change)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'user', 'appointment_date', 'status')  # Replace with actual fields
    list_filter = ('status', 'appointment_date')  # Add filters
    search_fields = ('doctor__user__username', 'user__username')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Doctor)
admin.site.register(Payment)
admin.site.register(Appointment, AppointmentAdmin)