from django import forms
from .models import Attachment

# Forms
class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['date', 'file', 'from_email_address', 'department']

