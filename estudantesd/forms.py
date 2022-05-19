from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Estudantes

class NovoEstudante(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
		help_texts={'username':'<br><br><li>Digite um Nome de Usuário Alfanumérico.<li>150 caracteres ou menos.<br><br>'}
		labels={'username':'Nome de Usuário'}
	def __init__(self,*args,**kwargs):
		super(NovoEstudante, self).__init__(*args, **kwargs)
		self.fields['password1'].help_text='''<br><br><li>Digite uma senha<li>Não pode conter informações similares às suas outras informações pessoais.
					   <li>No mínimo 8 caracteres.<br><br>'''
		self.fields['password1'].label='Senha'
		self.fields['password2'].help_text='<br><br><li>Confirme a senha digitada anteriormente.<br><br>'
		self.fields['password2'].label='Confirmação de Senha'
		self.fields['email'].help_text='<br><br><li>Digite um E-mail válido.<br><br>'
	def save(self, commit=True):
		user = super(NovoEstudante, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
class EstudanteForm(forms.ModelForm):
	class Meta:
		model=Estudantes
		fields=('Nome','RA','CEP','Email','renda','cod_curso','escola','cor','sexo','motivacao')
	def save(self, commit=True):
	  user = super(EstudanteForm, self).save(commit=False)
	  if commit:
	    user.save()
	  return user
