from asyncio import constants
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from exames.models import SolicitacaoExames


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
