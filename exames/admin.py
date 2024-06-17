from django.contrib import admin
from .models import PedidosExames, SolicitacaoExames, TiposExames, AcessoMedico

admin.site.register(TiposExames)
admin.site.register(SolicitacaoExames)
admin.site.register(PedidosExames)
admin.site.register(AcessoMedico)