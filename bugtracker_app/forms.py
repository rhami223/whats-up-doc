from django import forms



class AddTicket(forms.Form):
    title = forms.CharField(max_length=80)
    description = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
