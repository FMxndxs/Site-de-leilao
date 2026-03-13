"""
models.py — Definicao dos modelos de dados do app Auctions.

Cada classe representa uma tabela no banco de dados SQLite.
O Django ORM converte essas classes em SQL automaticamente.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuario. Herda de AbstractUser, que ja fornece
    campos padrao como username, email, password, is_active, etc.
    O campo 'watchlist' e acessivel via related_name no model Listing.
    """
    pass


class Category(models.Model):
    """
    Categoria de um anuncio (ex: Moda, Eletronicos, Esportes).
    Cada anuncio pode pertencer a uma categoria opcionalmente.
    """
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Listing(models.Model):
    """
    Anuncio de leilao. E o modelo central da aplicacao.

    Campos:
        title         — Titulo do anuncio
        description   — Descricao detalhada do item
        starting_bid  — Valor minimo do primeiro lance
        image_url     — URL de imagem do produto (opcional)
        category      — FK para Category (opcional, SET_NULL ao deletar)
        creator       — FK para User que criou o anuncio
        active        — Se o leilao esta aberto (True) ou encerrado (False)
        watchers      — ManyToMany com User para lista de favoritos
        created_at    — Data/hora de criacao (preenchido automaticamente)

    Metodo current_price():
        Retorna o maior lance existente ou o lance inicial se ninguem deu lance.
    """
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="listings"
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings"
    )
    active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(
        User, blank=True, related_name="watchlist"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def current_price(self):
        """Retorna o preco atual: maior lance ou lance inicial."""
        top_bid = self.bids.order_by("-amount").first()
        if top_bid:
            return top_bid.amount
        return self.starting_bid


class Bid(models.Model):
    """
    Lance em um anuncio.

    Campos:
        amount     — Valor do lance (decimal com 2 casas)
        bidder     — FK para User que fez o lance
        listing    — FK para Listing onde o lance foi dado
        created_at — Data/hora do lance
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} deu lance de R${self.amount} em {self.listing}"


class Comment(models.Model):
    """
    Comentario em um anuncio.

    Campos:
        text       — Texto do comentario
        commenter  — FK para User que comentou
        listing    — FK para Listing comentado
        created_at — Data/hora do comentario
    """
    text = models.TextField()
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter} em {self.listing}: {self.text[:50]}"
