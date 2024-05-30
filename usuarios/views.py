from django.shortcuts import redirect, render
from django.http import HttpResponse

def cadastro(request):

  if request.method == 'GET':
    return render(request, 'cadastro.html')
  
  elif request.method == 'POST':
    primeiro_nome = request.POST.get('primeiro_nome')
    segundo_nome = request.POST.get('segundo_nome')
    username = request.POST.get('username')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')

    if not senha == confirmar_senha:
      return redirect('/usuarios/cadastro')

    return HttpResponse(f'{username} - {email}')
