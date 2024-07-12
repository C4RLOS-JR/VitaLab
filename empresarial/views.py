from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from exames.models import SolicitacaoExames
from .utils import gerar_pdf_exames, gerar_senha_aleatoria


@staff_member_required # Se for membro da equipe
def gerenciar_clientes(request):
  clientes = User.objects.filter(is_staff=False)
  nome = request.GET.get('nome')
  email = request.GET.get('email')

  if nome:
    clientes = clientes.annotate(nome_completo=Concat('first_name', Value(' '), 'last_name')).filter(nome_completo__contains=nome) # O annotate cria um campo na 'models' em tempo de execução.
  if email:
    clientes = clientes.filter(email__contains=email)

  return render(request, 'gerenciar_clientes.html', {'clientes': clientes})

@staff_member_required
def cliente(request, cliente_id):
  cliente = User.objects.get(id=cliente_id)
  exames = SolicitacaoExames.objects.filter(usuario=cliente)

  return render(request, 'cliente.html', {'cliente': cliente,'exames': exames})

@staff_member_required
def exame_cliente(request, exame_id):
  exame = SolicitacaoExames.objects.get(id=exame_id)

  return render(request, 'exame_cliente.html', {'exame': exame})

def proxy_pdf(request, exame_id):
  exame = SolicitacaoExames.objects.get(id=exame_id)
  resultado = exame.resultado.open()

  return HttpResponse(resultado)

def gerar_senha(request, exame_id):
  exame = SolicitacaoExames.objects.get(id=exame_id)

  if not exame.senha:
    exame.senha = gerar_senha_aleatoria(6)
    exame.save()
    
  return FileResponse(gerar_pdf_exames(exame, exame.usuario, exame.senha), filename=f'{exame.usuario.first_name} - {exame.exame.nome}.pdf')

def alterar_dados_exame(request, exame_id):
  exame = SolicitacaoExames.objects.get(id=exame_id)
  pdf = request.FILES.get('resultado')
  status = request.POST.get('status')
  requer_senha = request.POST.get('requer_senha')

  if requer_senha and (not exame.senha):
    messages.add_message(request, constants.ERROR, 'Para exigir a senha é preciso gerar uma!')
    return redirect(f'/empresarial/exame_cliente/{exame_id}')

  if pdf:
    exame.resultado = pdf
  
  exame.status = status
  exame.requer_senha = True if requer_senha else False

  exame.save()
  messages.add_message(request, constants.SUCCESS, 'Dados alterados com sucesso!')

  return redirect(f'/empresarial/exame_cliente/{exame_id}')
