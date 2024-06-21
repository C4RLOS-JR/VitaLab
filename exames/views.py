from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidosExames, SolicitacaoExames, AcessoMedico
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

@login_required
def cancelar_pedido(request, pedido_id):
  pedido = PedidosExames.objects.get(id=pedido_id)

  if pedido.usuario == request.user:
    pedido.agendado = False
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido cancelado com sucesso!')
  else:
    messages.add_message(request, constants.ERROR, 'Esse pedido não é seu!')

  return redirect('/exames/gerenciar_pedidos')

@login_required
def gerenciar_exames(request):
  solicitacao_exames = SolicitacaoExames.objects.filter(usuario=request.user)

  return render(request, 'gerenciar_exames.html', {
    'solicitacao_exames': solicitacao_exames,
  })

@login_required
def resultado_exame(request, exame_id):
  exame = SolicitacaoExames.objects.get(id=exame_id)

  if not exame.resultado:
    messages.add_message(request, constants.ERROR, 'O resultado ainda não está disponível!...Tente novamente mais tarde.')
    return redirect('/exames/gerenciar_exames')
  if not exame.requer_senha:
    return redirect(exame.resultado.url)
  
  return redirect(f'/exames/solicitar_senha_exame/{exame_id}')

@login_required
def solicitar_senha_exame(request, exame_id):
  exame = SolicitacaoExames.objects.get(id=exame_id)

  if request.method == 'GET':
    return render(request, 'solicitar_senha_exame.html', {'exame': exame})
  elif request.method == 'POST':
    senha = request.POST.get('senha')
    
    if senha != exame.senha:
      messages.add_message(request, constants.ERROR, 'Senha inválida!')
      return redirect(f'/exames/solicitar_senha_exame/{exame_id}')
    
    return redirect(exame.resultado.url)
  
@login_required
def gerar_acesso_medico(request):
  if request.method == 'GET':
    acessos_medicos = AcessoMedico.objects.filter(usuario=request.user)

    return render(request, 'gerar_acesso_medico.html', {'acessos_medicos': acessos_medicos})
  elif request.method == 'POST':
    identificacao = request.POST.get('identificacao')
    tempo_de_acesso = request.POST.get('tempo_de_acesso')
    data_exame_inicial = request.POST.get('data_exame_inicial')
    data_exame_final = request.POST.get('data_exame_final')

    acesso_medico = AcessoMedico(
      usuario=request.user,
      identificacao=identificacao,
      tempo_de_acesso=tempo_de_acesso,
      data_exames_iniciais=data_exame_inicial,
      data_exames_finais=data_exame_final,
      criado_em=datetime.now()
    )
    acesso_medico.save()
    messages.add_message(request, constants.SUCCESS, 'Acesso médico gerado com sucesso!')

    return redirect('/exames/gerar_acesso_medico')