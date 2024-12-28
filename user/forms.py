from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import  UsernameField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth.forms import  SetPasswordForm
from django.contrib.auth.forms import   PasswordResetForm
from django.contrib.auth.models import User
import requests
from .models import ContactMessage, Customer
from django.core.validators import validate_email
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.core.mail import send_mail
import re
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}), required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}), required=True)





class CustomerRegistrationForm(UserCreationForm):
    firstname = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'oninput': 'validateName(this)', 'placeholder': 'Enter your first name'}),
    )
    lastname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'validateName(this)', 'placeholder': 'Enter your last name'}),
    )
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}))
    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].error_messages = {'required': 'Firstname is required.'}
        self.fields['lastname'].error_messages = {'required': 'Lastname is required.'}
        self.fields['username'].error_messages = {'required': 'Username is required.'}
        self.fields['email'].error_messages = {'required': 'Email is required.'}
        self.fields['password1'].error_messages = {'required': 'Password1 is required.'}
        self.fields['password2'].error_messages = {'required': 'Password2 is required.'}
        
    
    def clean_firstname(self):
        firstname = self.cleaned_data.get('firstname', '')

        
        if not firstname.replace(' ', '').isalpha():
            raise forms.ValidationError('Invalid characters in firstname.')

        
        if len(firstname) >= 25:
            raise forms.ValidationError('Firstname length exceeds 25 characters.')

        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname', '')

       
        if not lastname.replace(' ', '').isalpha():
            raise forms.ValidationError('Invalid characters in lastname.')

        
        if len(lastname) >= 25:
            raise forms.ValidationError('Lastname length exceeds 25 characters.')

        return lastname

   
    from django.core.exceptions import ValidationError

    def clean_email(self):
        email = self.cleaned_data.get('email')

        print("Original email:", email)

        # Check for dot or space at the beginning of the email
        if email.startswith('.') or email.startswith(' '):
            raise forms.ValidationError("Email should not start with a dot or space.")

        # Validate the email using Django's built-in email validator
        try:
            validate_email(email)
        except forms.ValidationError as e:
            print("Validation error:", e)
            raise forms.ValidationError("Invalid email format.")

        return email



    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Send a welcome email to the user
            send_mail(
                'Welcome to Our Website',
                'Thank you for registering on ClickShop. We appreciate your interest.',
                'kaneshk552@gmail.com',
                [user.email],
                fail_silently=False,
            )
        return user
   

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

       
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')

       
        if not re.search(r'[a-z]', password1):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')

        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError('Password must contain at least one special character.')

       
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')

        return password1
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')

       
        if not re.search(r'[A-Z]', password2):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')

       
        if not re.search(r'[a-z]', password2):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')

        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password2):
            raise forms.ValidationError('Password must contain at least one special character.')

       
        if len(password2) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')

        return password2

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'password1', 'password2']
       



class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-Password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-Password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-Password','class':'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    
from django import forms
from .models import Customer
import requests

class CustomerProfileForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Enter your name'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Gender'}))
    Address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}))
    pincode = forms.CharField(max_length=6, min_length=6, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your pincode'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your country'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your state'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city'}))
    mobile = forms.CharField(max_length=10, min_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}))
    
    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {'required': 'Name is required.'}
        self.fields['Address'].error_messages = {'required': 'Address is required.'}
        self.fields['pincode'].error_messages = {'required': 'Pincode is required.'}
        self.fields['country'].error_messages = {'required': 'Country is required.'}
        self.fields['state'].error_messages = {'required': 'State is required.'}
        self.fields['city'].error_messages = {'required': 'City is required.'}
        self.fields['mobile'].error_messages = {'required': 'Mobile is required.'}
        self.fields['gender'].error_messages = {'required': 'Gender is required.'}

    def clean_state(self):
        state = self.cleaned_data.get('state')
        country = self.cleaned_data.get('country')

        if country and not state:
            raise forms.ValidationError("State is required if the country is selected.")

        if not state:
            return state

        if any(char.isdigit() for char in state):
            raise forms.ValidationError("State should not contain numbers.")

        return state

    def clean_city(self):
        city = self.cleaned_data.get('city')
        country = self.cleaned_data.get('country')
        state = self.cleaned_data.get('state')

        if country and state and not city:
            raise forms.ValidationError("City is required if the country and state are selected.")

        if not city:
            return city

        if any(char.isdigit() for char in city):
            raise forms.ValidationError("City should not contain numbers.")

        return city

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not str(mobile).isdigit() or len(str(mobile)) != 10 or not str(mobile).startswith(('6', '7', '8', '9')):
            raise forms.ValidationError("Please enter a valid 10-digit mobile number starting with 6, 7, 8, or 9.")
        return mobile

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not str(pincode).isdigit() or len(str(pincode)) != 6:
            raise forms.ValidationError("Please enter a valid 6-digit pincode.")
        return pincode

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("This Name field is required.")
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name should not contain numbers.")
        return name
    
    def clean_address(self):
        address = self.cleaned_data.get('Address')
        if not address:
            raise forms.ValidationError("This Address is required.")
        return address

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise forms.ValidationError("Country is required.")
        return country

    class Meta:
        model = Customer
        fields = ['name', 'gender', 'Address', 'pincode', 'country', 'state', 'city', 'mobile']




class YourForm(forms.Form):
   
    delete_Address = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        



# forms.py
from django import forms

class ProductFilterForm(forms.Form):
    name = forms.CharField(required=False)
    price = forms.DecimalField(required=False, min_value=0)
    brand = forms.CharField(required=False)

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, max_value=5, label='Rating',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Comment'
    )

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')

        # Add additional validation or cleaning if needed

        return comment

    class Meta:
        model = Review
        fields = ['rating', 'comment']



# forms.py
from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['email', 'message']






