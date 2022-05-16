from django.urls import path
from . import views

urlpatterns=[
   path('',views.homepage,name='home'),
   path('lista_admin',views.index,name='index'),
   path('add/',views.add,name='add'),
   path('registro',views.addrecord,name='addrecord'),
   path('delete/<int:id>',views.delete,name='delete'),
   path('update/<int:id>',views.update,name='update'),
   path('update/<int:id>/updaterecord',views.updaterecord,name='updaterecord'),
   path('register',views.register,name='register'),
   path('perfil',views.perfil,name='perfil'),
   path('perfil_dados',views.perfil_dados,name='perfil_dados'),
   path('perfil_sol',views.perfil_sol,name='perfil_sol'),
   path('delete_est',views.delete_owned,name='delete_est'),
   path('update_owned',views.update_owned,name='update_owned'),
   path('sol_feita',views.sol_feita,name='sol_feita'),
   path('fazer_solicitacao',views.fazer_solicitacao,name='fazer_solicitacao'),
   path('lista_solicitacoes',views.lista_solicitacoes,name='lista_solicitacoes'),
   path('delete_sol/<int:id>',views.delete_sol,name='delete_sol'),]
