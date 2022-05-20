from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Estudantes,Solicitacao
from django.urls import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from . import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from . import processar
# Create your views here.
def supuser(user):
    return user.is_superuser

@user_passes_test(supuser)
def index(request):
    lista_estudantes=Estudantes.objects.all().values()
    template= loader.get_template('lista_estudantes.html')
    context= {'lista_estudantes':lista_estudantes}
    return HttpResponse(template.render(context,request))
@user_passes_test(supuser)
def lista_solicitacoes(request):
    lista_solicitacoes=Solicitacao.objects.all().values()
    template= loader.get_template('lista_solicitacoes.html')
    context= {'lista_solicitacoes':lista_solicitacoes}
    return HttpResponse(template.render(context,request))
@login_required
def add(request):
    return HttpResponseRedirect('/registro')

@login_required
def addrecord(request):
     if request.method == "POST":
       form = forms.EstudanteForm(request.POST)
       if form.is_valid():
         if request.POST.get('Email')==request.user.email:
           user = form.save()
           return HttpResponseRedirect('/')
         else:
           messages.error(request,'E-mail não corresponde ao E-mail usado no registro de usuário.')
       messages.error(request,"Registro Falhou, Informações Inválidas")
     form = forms.EstudanteForm()
     context={"register_form":form}
     template= loader.get_template('add.html')
     return HttpResponse(template.render(context,request))

@user_passes_test(supuser)
def delete(request, id):
    estudante= Estudantes.objects.get(id=id)
    if estudante.sol_feita:
        solicitacao= Solicitacao.objects.get(RA=estudante.RA)
        solicitacao.delete()
    estudante.delete()
    return HttpResponseRedirect(reverse('index'))
@user_passes_test(supuser)
def delete_sol(request,id):
    solicitacao= Solicitacao.objects.get(id=id)
    estudante= Estudantes.objects.get(RA=solicitacao.RA)
    solicitacao.delete()
    estudante.sol_feita = False
    estudante.save()
    return HttpResponseRedirect(reverse('lista_solicitacoes'))

@user_passes_test(supuser)
def update(request, id):
    estudante= Estudantes.objects.get(id=id)
    template= loader.get_template('update.html')
    context={'estudante':estudante}
    return HttpResponse(template.render(context,request))

@user_passes_test(supuser)
def updaterecord(request,id):
    Nome=request.POST['Nome']
    RA=request.POST['RA']
    CEP=request.POST['CEP']
    Email=request.POST['Email']
    renda=request.POST['renda']
    cod_curso=request.POST['cod_curso']
    escola=request.POST['escola']
    cor=request.POST['cor']
    sexo=request.POST['sexo']
    motivacao=request.POST['motivacao']
    sol_feita=request.POST.get('sol_feita',False)
    estudante=Estudantes.objects.get(id=id)
    estudante.Nome=Nome
    estudante.RA=RA
    estudante.CEP=CEP
    estudante.Email=Email
    estudante.renda=renda
    estudante.cod_curso=cod_curso
    estudante.escola=escola
    estudante.cor=cor
    estudante.sexo=sexo
    estudante.motivacao=motivacao
    if sol_feita=='on':
        estudante.sol_feita=True
    else:
        estudante.sol_feita=False
    estudante.save()
    return HttpResponseRedirect(reverse('index'))

def homepage(request):
    template=loader.get_template('homepage.html')
    return HttpResponse(template.render(request=request))

def register(request):
  if request.method == "POST":
    form = forms.NovoEstudante(request.POST)
    if form.is_valid():
      user = form.save()
      return HttpResponseRedirect('/')
    messages.error(request,form.errors)
  form = forms.NovoEstudante()
  context={"register_form":form}
  template= loader.get_template('registration/register.html')
  return HttpResponse(template.render(context,request))

@login_required
def perfil(request):
    est_emails=Estudantes.objects.values_list('Email',flat=True)
    if request.user.email in est_emails:
        estudante= Estudantes.objects.get(Email=request.user.email)
        context={'estudante':estudante,'est_emails':est_emails}
    else:
        context={'estudante':None,'est_emails':est_emails}
    template=loader.get_template('perfil_main.html')
    return HttpResponse(template.render(context,request))

@login_required
def perfil_dados(request):
    est_emails=Estudantes.objects.values_list('Email',flat=True)
    if request.user.email in est_emails:
        estudante= Estudantes.objects.get(Email=request.user.email)
        context={'estudante':estudante,'est_emails':est_emails}
    else:
        context={'estudante':None,'est_emails':est_emails}
    template=loader.get_template('perfil_dados.html')
    return HttpResponse(template.render(context,request))
@login_required
def perfil_sol(request):
    est_emails=Estudantes.objects.values_list('Email',flat=True)
    if request.user.email in est_emails:
        estudante= Estudantes.objects.get(Email=request.user.email)
        context={'estudante':estudante,'est_emails':est_emails}
    else:
        context={'estudante':None,'est_emails':est_emails}
    template=loader.get_template('perfil_sol.html')
    return HttpResponse(template.render(context,request))
@login_required
def delete_owned(request):
    est_emails=Estudantes.objects.values_list('Email',flat=True)
    if request.user.email in est_emails:
        estudante= Estudantes.objects.get(Email=request.user.email)
        if estudante.sol_feita:
            solicitacao= Solicitacao.objects.get(RA=estudante.RA)
            solicitacao.delete()
        estudante.delete()
        return HttpResponseRedirect(reverse('perfil'))
    else:
        messages.error(request,'Você não tem um Registro de Estudante.')
        return HttpResponseRedirect('/registro')
@login_required
def update_owned(request):
    if request.method == 'POST':
      est_emails=Estudantes.objects.values_list('Email',flat=True)
      if request.user.email in est_emails:
          estudante= Estudantes.objects.get(Email=request.user.email)
          Nome=request.POST['Nome']
          RA=request.POST['RA']
          CEP=request.POST['CEP']
          Email=request.POST['Email']
          renda=request.POST['renda']
          cod_curso=request.POST['cod_curso']
          escola=request.POST['escola']
          cor=request.POST['cor']
          sexo=request.POST['sexo']
          motivacao=request.POST['motivacao']
          estudante.Nome=Nome
          estudante.RA=RA
          estudante.CEP=CEP
          estudante.Email=Email
          estudante.renda=renda
          estudante.cod_curso=cod_curso
          estudante.escola=escola
          estudante.cor=cor
          estudante.sexo=sexo
          estudante.motivacao=motivacao
          estudante.sol_feita=False
          estudante.save()
          return HttpResponseRedirect('/perfil_dados')
      else:
          messages.error(request,'Você não tem um Registro de Estudante.')
          return HttpResponseRedirect('/registro')
    else:
        est_emails=Estudantes.objects.values_list('Email',flat=True)
        if request.user.email in est_emails:
            estudante= Estudantes.objects.get(Email=request.user.email)
            context={'estudante':estudante}
            template= loader.get_template('atualizar.html')
            return HttpResponse(template.render(context,request))
        else:
            messages.error(request,'Você não possui um perfil de estudante')
            return HttpResponseRedirect('/registro')

@login_required
def fazer_solicitacao(request):
    est_emails=Estudantes.objects.values_list('Email',flat=True)
    if request.user.email in est_emails:
        estudante= Estudantes.objects.get(Email=request.user.email)

        deferida= processar.Classificar(estudante.RA,estudante.renda,estudante.escola,estudante.motivacao,estudante.cod_curso,
                                       estudante.cor,estudante.sexo)
        Notebook= processar.ModeloNotebook(estudante.cod_curso)

        mensagem_mime = processar.FazerMensagem(estudante.Email,deferida,estudante.Nome,estudante.RA,Notebook)[0]

        mensagem_txt= processar.FazerMensagem(estudante.Email,deferida,estudante.Nome,estudante.RA,Notebook)[1]

        email_enviado= processar.enviar_email(mensagem_mime,estudante.Email)

        sol= Solicitacao(Nome=estudante.Nome,RA=estudante.RA,Email=estudante.Email,
                         Notebook=Notebook,Deferida=deferida,Mensagem= 'Email Pronto' ,EmailEnviado=email_enviado)
        sol.save()

        estudante.sol_feita=True
        estudante.save()
        return HttpResponseRedirect('/sol_feita')

    else:
        messages.error(request,'Você não tem um Registro de Estudante.')
        return HttpResponseRedirect('/registro')

@login_required
def sol_feita(request):
    est_emails=Estudantes.objects.values_list('Email',flat=True)
    if request.user.email in est_emails:
        estudante= Estudantes.objects.get(Email=request.user.email)
        if estudante.sol_feita:
            solicitacao = Solicitacao.objects.get(RA=estudante.RA)
            context= {'estudante':estudante,'solicitacao':solicitacao}
        else:
            context= {'estudante':estudante}
        template= loader.get_template('solicitacao.html')
        return HttpResponse(template.render(context,request))
    else:
        messages.error(request,'Você não tem um Registro de Estudante.')
        return HttpResponseRedirect('/registro')
def slideshow(request):
    template=loader.get_template('slideshow.html')
    return HttpResponse(template.render(request=request))
