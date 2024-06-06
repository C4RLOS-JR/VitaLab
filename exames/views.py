from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidosExames, SolicitacaoExames
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants

@login_required
def solicitar_exames(request):
  exames = TiposExames.objects.all()
  
  if request.method == 'GET':
    return render(request, 'solicitar_exames.html', {'exames': exames})
  elif request.method == 'POST':
    exames_id = request.POST.getlist('exames_selecionados')
    exames_solicitados = TiposExames.objects.filter(id__in=exames_id)    
    preco_total = 0
    data = datetime.now()

    for exame in exames_solicitados:
      if exame.disponivel:
        preco_total += exame.preco

    return render(request, 'solicitar_exames.html', {
      'exames': exames,
      'exames_solicitados': exames_solicitados,
      'preco_total':preco_total,
      'data': data
    })

@login_required
def fechar_pedido(request):
  exames_id = request.POST.getlist('exames')
  solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

  pedido_exame = PedidosExames(
    usuario = request.user,
    data = datetime.now()
  )
  pedido_exame.save()

  for exame in solicitacao_exames:
    solicitacao_exames_temp = SolicitacaoExames(
      usuario = request.user,
      exame = exame,
      status = 'E',
    )
    solicitacao_exames_temp.save()
    pedido_exame.exames.add(solicitacao_exames_temp)

  pedido_exame.save()
  messages.add_message(request, constants.SUCCESS, 'Pedido de exame realizado com sucesso!')

  return redirect('/exames/gerenciar_pedidos')

@login_required
def gerenciar_pedidos(request):
  pedidos_exames = PedidosExames.objects.filter(usuario=request.user)

  return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})
