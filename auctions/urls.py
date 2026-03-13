"""
urls.py — Mapeamento de URLs para as views do app Auctions.

Cada path() conecta um padrao de URL a uma funcao de view.
O parametro 'name' permite referenciar a rota nos templates com {% url 'name' %}.
"""

from django.urls import path

from . import views

urlpatterns = [
    # Pagina inicial — lista de anuncios ativos
    path("", views.index, name="index"),

    # Autenticacao
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Criacao de anuncio (requer login)
    path("create", views.create_listing, name="create"),

    # Pagina de detalhe de um anuncio
    path("listings/<int:listing_id>", views.listing_page, name="listing"),

    # Acoes em um anuncio (todas requerem login)
    path("listings/<int:listing_id>/watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("listings/<int:listing_id>/bid", views.place_bid, name="place_bid"),
    path("listings/<int:listing_id>/close", views.close_auction, name="close_auction"),
    path("listings/<int:listing_id>/comment", views.add_comment, name="add_comment"),

    # Pagina de favoritos do usuario (requer login)
    path("watchlist", views.watchlist, name="watchlist"),

    # Categorias
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_listings, name="category_listings"),
]
