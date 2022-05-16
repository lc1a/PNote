import ProjetoNotebook
import pickle
import numpy as np
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

def Classificar(ra,renda,escola,motivacao,cod_curso,cor,sexo):
    with open('estudantesd/ModeloTreinado.pickle',mode='rb') as file:
        Modelo = pickle.load(file)

    #Calculando Nota Normalizada:
    nn_df=pd.DataFrame({'matrícula':[ra],'renda':[renda],'escola':[escola],
                     'motivação':[motivacao],'cod_curso':[cod_curso],'cor':[cor],
                    'sexo':[sexo]}).set_index('matrícula')

    nn= ProjetoNotebook.Analista.NotasNormalizadas(tbcp=nn_df).Criar()
    nn_arr=nn.to_numpy()[0]
    nota_normalizada=nn_arr

    #Calculando Média Ponderada:
    mp=np.dot(nota_normalizada,Modelo.inst_NP.pesos)/np.array([sum(Modelo.inst_NP.pesos)])

    #Classifcando como deferido ou não utilizando o modelo treinado da instância da classe FiltragemKMeans
    clas_def = lambda x: 1 if x==0 else 0
    clas=clas_def(Modelo.classificar(mp)[0])
    if clas==1:
        deferido=True
    else:
        deferido=False
    return deferido

def ModeloNotebook(cod_curso):
    if cod_curso==1 or cod_curso==8 or cod_curso==7:
        modelo='latitude'
    elif cod_curso==6 or cod_curso==3 or cod_curso==2:
        modelo='vostro'
    elif cod_curso==9 or cod_curso==5 or cod_curso==4:
        modelo='inspiron'
    return modelo

def FazerMensagem(email,deferido,nome,ra,notebook=None):

    sender_email = "projetonotebookcdia@gmail.com"
    receiver_email= email
    message=MIMEMultipart('alternative')
    message['Subject']='Resposta Referente a sua Solicitação de Compra de Notebook'
    message['From']= sender_email
    message['To']= receiver_email

    if deferido==True:
      MensagemDoEmailTxt=f"""\
      Olá {nome}, Tudo bem?
      A universidade PUC-SP manda este e-mail com felicidade para informá-lo que a sua solicitação de compra de notebook foi deferida!
      Queremos oferecer a nossos estudantes todas as oportunidades e ferramentas necessárias para seu sucesso
      e por isso já realizamos a compra do seu notebook de modelo {notebook} da marca Dell que será enviado ao seu endereço fornecido
      na matrícula.

      Mensagem Enviada Automaticamente por: ProjetoNotebook, para o aluno de RA: {ra}."""

      MensagemDoEmailHtml=f"""\
      <html>
        <body>
          <h1>Olá <strong>{nome}</strong>,Tudo Bem?</h1><br>
          <h2>A Universidade <strong><a href="https://www.pucsp.br/home">PUC-SP</a></strong> manda este e-mail com felicidade para informá-lo<br>
          que a sua solicitação de compra de notebook foi <strong>Deferida!</strong><br></h2>
          <h3>Queremos oferecer a nossos estudantes todas as oportunidades e ferramentas necessárias para seu sucesso<br>
          e por isso <strong>Já realizamos a compra do seu notebook</strong><br></h3>
          <h3><strong>Modelo:</strong> <em>{notebook}</em><br>
          <strong>Da Marca:</strong> <em><a href="https://www.dell.com/pt-br">DELL</a></em><br>
          Que será enviado ao seu endereço fornecido na matrícula.<br></h3>

          <h3>Mensagem Enviada Automáticamente<br>
          <strong>Por:</strong> <em>ProjetoNotebook</em><br>
          <strong>Para:</strong> Aluno de RA: <em>{ra}</em></h3>
        </body>
      </html>
      """

    else:

      MensagemDoEmailTxt=f"""\
      Olá {nome}, Tudo bem?
      A universidade PUC-SP manda este e-mail para informá-lo que a sua solicitação de compra de notebook não
      foi deferida.
      Sentimos muito por não ser possível atender a sua solicitação no momento.
      Mensagem Enviada Automaticamente por: ProjetoNotebook, para o aluno de RA: {ra}."""

      MensagemDoEmailHtml=f"""\
      <html>
        <body>
          <h1>Olá <strong>{nome}</strong>,Tudo Bem?</h1><br>
          <h2>A Universidade <strong><a href="https://www.pucsp.br/home">PUC-SP</a></strong> manda este e-mail para informá-lo<br>
          que a sua solicitação de compra de notebook <strong>Não Foi Deferida.</strong><br></h2>
          <h3>Sentimos Muito por não ser possível atender sua solicitação no momento.</h3><br>
          <h3>Mensagem Enviada Automáticamente<br>
          <strong>Por:</strong> <em>ProjetoNotebook</em><br>
          <strong>Para:</strong> Aluno de RA: <em>{ra}</em></h3>
        </body>
      </html>
      """
    part1=MIMEText(MensagemDoEmailTxt,'plain')
    part2=MIMEText(MensagemDoEmailHtml,'html')
    message.attach(part1)
    message.attach(part2)
    mensagem_personalizada=MensagemDoEmailTxt
    return message,mensagem_personalizada

def enviar_email(mensagem,email):
    '''método "enviar_email" da instância que tem a função de:
    Enviar um e-mail para o e-mail do estudante fornecido a partir da conta 'projetonotebookcdia@gmail.com' com a mensagem
    personalizada criada. Utilizando a biblioteca 'smtp' e 'ssl' inclusas no python.
    Não será executado caso o método "criar_mensagem_email" da instância ainda não tiver sido executado.
    '''
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "projetonotebookcdia@gmail.com"
    password = "a3sQ2pw3C1#Rz"
    receiver_email= email
    context = ssl.create_default_context()
    try:
      server = smtplib.SMTP(smtp_server,port)
      server.starttls(context=context)
      server.login(sender_email, password)
      message = mensagem.as_string()
      server.sendmail(sender_email,receiver_email,message)
      resp=True
    except Exception as e:
      resp=False
    finally:
      server.quit()
      return resp
