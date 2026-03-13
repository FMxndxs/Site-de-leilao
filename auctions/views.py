"""
views.py — Funcoes de view (controladores) do app Auctions.

Cada funcao recebe um HttpRequest e retorna um HttpResponse.
O decorator @login_required redireciona usuarios nao autenticados
para a pagina de login antes de acessar a view protegida.
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment


# =====================================================================
# PAGINAS PUBLICAS
# =====================================================================

def index(request):
    """
    Pagina inicial — exibe todos os anuncios ativos ordenados
    do mais recente para o mais antigo.
    """
    listings = Listing.objects.filter(active=True).order_by("-created_at")
    return render(request, "auctions/index.html", {
        "listings": listings,
        "heading": "Anuncios Ativos"
    })


def listing_page(request, listing_id):
    """
    Pagina de detalhe de um anuncio especifico.

    Calcula e passa para o template:
      - is_watching   : se o usuario logado tem este item nos favoritos
      - is_creator    : se o usuario logado e o dono do anuncio
      - bid_count     : quantidade total de lances
      - is_winner     : se o leilao encerrou e o usuario logado venceu
      - is_top_bidder : se o lance mais alto e do usuario logado
      - comments      : todos os comentarios do anuncio
    """
    listing = get_object_or_404(Listing, pk=listing_id)
    is_watching = (
        request.user.is_authenticated
        and listing.watchers.filter(pk=request.user.pk).exists()
    )
    is_creator = (
        request.user.is_authenticated
        and request.user == listing.creator
    )

    bid_count = listing.bids.count()
    top_bid = listing.bids.order_by("-amount").first()

    # Verifica se o usuario logado venceu o leilao (somente se encerrado)
    is_winner = (
        not listing.active
        and top_bid is not None
        and request.user.is_authenticated
        and top_bid.bidder == request.user
    )

    # Verifica se o usuario logado tem o maior lance atual
    is_top_bidder = (
        top_bid is not None
        and request.user.is_authenticated
        and top_bid.bidder == request.user
    )

    comments = listing.comments.order_by("-created_at")

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watching": is_watching,
        "is_creator": is_creator,
        "bid_count": bid_count,
        "is_winner": is_winner,
        "is_top_bidder": is_top_bidder,
        "comments": comments,
    })


def categories(request):
    """Exibe a lista de todas as categorias em ordem alfabetica."""
    all_categories = Category.objects.all().order_by("name")
    return render(request, "auctions/categories.html", {
        "categories": all_categories
    })


def category_listings(request, category_id):
    """Exibe apenas os anuncios ativos de uma categoria especifica."""
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(
        active=True, category=category
    ).order_by("-created_at")
    return render(request, "auctions/index.html", {
        "listings": listings,
        "heading": f"Anuncios Ativos em {category.name}"
    })


# =====================================================================
# AUTENTICACAO
# =====================================================================

def login_view(request):
    """
    GET  — renderiza o formulario de login.
    POST — autentica o usuario e redireciona para a pagina inicial.
           Se falhar, exibe mensagem de erro.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Usuario e/ou senha invalidos."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    """Desloga o usuario e redireciona para a pagina inicial."""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    GET  — renderiza o formulario de cadastro.
    POST — cria um novo usuario. Valida se as senhas coincidem
           e se o username ja nao esta em uso.
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "As senhas devem ser iguais."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Este usuario ja esta em uso."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# =====================================================================
# ACOES DO USUARIO AUTENTICADO
# =====================================================================

@login_required
def create_listing(request):
    """
    GET  — renderiza o formulario de criacao de anuncio.
    POST — valida os campos e cria o anuncio no banco.
           Redireciona para a pagina do novo anuncio apos sucesso.

    Campos obrigatorios: titulo, descricao, lance inicial.
    Campos opcionais: URL da imagem, categoria.
    """
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        starting_bid = request.POST.get("starting_bid", "")
        image_url = request.POST.get("image_url", "").strip()
        category_id = request.POST.get("category", "")

        # Validacao de campos obrigatorios
        if not title or not description or not starting_bid:
            return render(request, "auctions/create_listing.html", {
                "categories": Category.objects.all(),
                "message": "Titulo, descricao e lance inicial sao obrigatorios."
            })

        # Validacao do valor do lance inicial
        try:
            starting_bid = float(starting_bid)
            if starting_bid < 0.01:
                raise ValueError
        except ValueError:
            return render(request, "auctions/create_listing.html", {
                "categories": Category.objects.all(),
                "message": "O lance inicial deve ser um numero positivo."
            })

        # Busca a categoria se informada
        category = None
        if category_id:
            category = Category.objects.filter(pk=category_id).first()

        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            creator=request.user
        )
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))

    # GET — exibe formulario com as categorias disponiveis
    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })


@login_required
def toggle_watchlist(request, listing_id):
    """
    Alterna o anuncio na lista de favoritos do usuario.
    Se ja esta nos favoritos, remove; senao, adiciona.
    Sempre redireciona de volta para a pagina do anuncio.
    """
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.watchers.filter(pk=request.user.pk).exists():
        listing.watchers.remove(request.user)
    else:
        listing.watchers.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def place_bid(request, listing_id):
    """
    Processa um novo lance em um anuncio.

    Regras de validacao:
      - Se nao ha lances, o valor deve ser >= lance inicial
      - Se ja ha lances, o valor deve ser > maior lance atual

    Em caso de erro, re-renderiza a pagina do anuncio com mensagem.
    Em caso de sucesso, cria o Bid e redireciona.
    """
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == "POST":
        try:
            bid_amount = float(request.POST.get("bid", 0))
        except (ValueError, TypeError):
            bid_amount = 0

        current = listing.current_price()
        bid_count = listing.bids.count()
        error = None

        # Primeiro lance: deve ser >= ao lance inicial
        if bid_count == 0 and bid_amount < float(current):
            error = f"O lance deve ser no minimo R$ {current}."
        # Lances subsequentes: deve ser > que o maior lance
        elif bid_count > 0 and bid_amount <= float(current):
            error = f"O lance deve ser maior que R$ {current}."

        if error:
            top_bid = listing.bids.order_by("-amount").first()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "is_watching": listing.watchers.filter(pk=request.user.pk).exists(),
                "is_creator": request.user == listing.creator,
                "bid_count": bid_count,
                "is_winner": False,
                "is_top_bidder": top_bid is not None and top_bid.bidder == request.user,
                "comments": listing.comments.order_by("-created_at"),
                "message": error,
            })

        # Lance valido — salva no banco
        Bid.objects.create(
            amount=bid_amount,
            bidder=request.user,
            listing=listing
        )
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def close_auction(request, listing_id):
    """
    Encerra o leilao. Somente o criador do anuncio pode encerrar.
    O maior lance no momento passa a ser o vencedor.
    """
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.creator:
        listing.active = False
        listing.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def add_comment(request, listing_id):
    """
    Adiciona um comentario ao anuncio.
    Ignora textos vazios. Redireciona de volta para a pagina do anuncio.
    """
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        text = request.POST.get("comment", "").strip()
        if text:
            Comment.objects.create(
                text=text,
                commenter=request.user,
                listing=listing
            )
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def watchlist(request):
    """
    Exibe todos os anuncios que o usuario adicionou aos favoritos.
    Reutiliza o template index.html com titulo diferente.
    """
    listings = request.user.watchlist.all().order_by("-created_at")
    return render(request, "auctions/index.html", {
        "listings": listings,
        "heading": "Meus Favoritos"
    })
