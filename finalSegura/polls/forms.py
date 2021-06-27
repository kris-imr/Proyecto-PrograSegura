from django import forms
from polls.models import Perfil

class UserForm(forms.ModelForm):
    password=forms.CharField(min_length=12, validators=[RegexValidator(regex=r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[$@$!%?&])[A-Za-z\d$@$!%?&]', message='La contraseña debe tener lo siguiente: minúsculas, MAYÚSCULAS, números, caractere especiales ($@$!%*?&) y ser 12')], widget=forms.PasswordInput)
    confirmar_password=forms.CharField(min_length=12, validators=[RegexValidator(regex=r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[$@$!%?&])[A-Za-z\d$@$!%?&]')], widget=forms.PasswordInput)
    class Meta:
        model = Perfil
        fields = ['username', 'first_name', 'last_name', 'email','Telefono', 'Token', 'chatID', 'password', 'confirmar_password']
        db_table = 'polls_perfil'
        help_texts = {k:"" for k in fields }