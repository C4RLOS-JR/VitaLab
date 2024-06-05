from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidosExames, SolicitacaoExames
from datetime import datetime
import calendar

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

def fechar_pedido(request):
  exames_id = request.POST.getlist('exames')

  pedido_exame = PedidosExames(
    usuario = request.user,
    data = datetime.now()
  )
  pedido_exame.save()

  return HttpResponse('teste')
