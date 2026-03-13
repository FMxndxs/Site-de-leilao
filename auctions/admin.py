"""
admin.py — Configuracao do painel administrativo Django.

Registra os modelos para que possam ser gerenciados via /admin/.
As classes *Admin personalizam quais colunas aparecem na listagem
e quais filtros ficam disponiveis na barra lateral.
"""

from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment

admin.site.site_header = "Administração Leilões"
admin.site.site_title = "Leilões"


class ListingAdmin(admin.ModelAdmin):
    """Exibe colunas uteis e filtros por status e categoria."""
    list_display = ("title", "creator", "starting_bid", "category", "active", "created_at")
    list_filter = ("active", "category")
    list_display_links = ("title",)
    search_fields = ("title", "description")
    ordering = ("-created_at",)


class BidAdmin(admin.ModelAdmin):
    """Exibe quem deu o lance, em qual anuncio e o valor."""
    list_display = ("bidder", "listing", "amount", "created_at")
    list_filter = ("listing",)
    ordering = ("-created_at",)


class CommentAdmin(admin.ModelAdmin):
    """Exibe o autor do comentario, o anuncio e a data."""
    list_display = ("commenter", "listing", "created_at")
    list_filter = ("listing",)
    ordering = ("-created_at",)


# Registro dos modelos no painel admin
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
