from django import forms
from .models import Employee, EmployeeAgreement, User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'form-control' class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Explicitly use 'RadioSelect' widget for Boolean fields
        for field in self.fields:
            if isinstance(self.fields[field], forms.BooleanField):
                self.fields[field].widget = forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])

    def clean_password(self):
        """
        Ensure password meets certain criteria (optional).
        """
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def save(self, commit=True):
        """
        Override the save method to hash the password before saving the instance.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'form-control' class to all fields for Bootstrap styling
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'form-control' class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Explicitly use 'RadioSelect' widget for Boolean fields
        for field in self.fields:
            if isinstance(self.fields[field], forms.BooleanField):
                self.fields[field].widget = forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])


class EmployeeAgreementForm(forms.ModelForm):
    class Meta:
        model = EmployeeAgreement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'form-control' class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Explicitly use 'RadioSelect' widget for Boolean fields
        for field in self.fields:
            if isinstance(self.fields[field], forms.BooleanField):
                self.fields[field].widget = forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])

