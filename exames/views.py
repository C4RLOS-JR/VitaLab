from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import TiposExames, SolicitacaoExames

@login_required
def solicitar_exames(request):
  exames = TiposExames.objects.all()
  
  if request.method == 'GET':
    return render(request, 'solicitar_exames.html', {'exames': exames})
  elif request.method == 'POST':
    exames_id = request.POST.getlist('exames_selecionados')
    exames_solicitados = TiposExames.objects.filter(id__in=exames_id)
    
    # Fazer : Calcular o preço somente dos exames disponíveis.
    preco_total = 0
    for exame in exames_solicitados:
      preco_total += exame.preco


    return render(request, 'solicitar_exames.html', {
      'exames': exames,
      'exames_solicitados': exames_solicitados,
      'preco_total':preco_total
    })
