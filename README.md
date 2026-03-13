# Commerce — Plataforma de Leiloes Online

Projeto desenvolvido para o curso **CS50's Web Programming with Python and JavaScript** (Projeto 2).

Uma aplicacao web de leiloes construida com **Django**, onde usuarios podem criar anuncios, dar lances, comentar e gerenciar favoritos.

---

## Estrutura do Projeto

```
Commerce/
├── commerce/                  # Configuracoes do projeto Django
│   ├── __init__.py
│   ├── settings.py            # Configuracoes gerais (banco, apps, auth)
│   ├── urls.py                # Roteamento raiz (inclui auctions.urls)
│   ├── wsgi.py                # Entry point WSGI
│   └── asgi.py                # Entry point ASGI
│
├── auctions/                  # App principal do leilao
│   ├── migrations/            # Migracoes do banco de dados
│   ├── static/auctions/
│   │   └── styles.css         # Estilizacao CSS (tema claro/escuro futurista)
│   ├── templates/auctions/
│   │   ├── layout.html        # Template base (navbar, tema, bloco body)
│   │   ├── index.html         # Listagem de anuncios (grid de cards)
│   │   ├── listing.html       # Pagina de detalhe do anuncio
│   │   ├── create_listing.html # Formulario de criacao de anuncio
│   │   ├── categories.html    # Grid de categorias
│   │   ├── login.html         # Pagina de login
│   │   └── register.html      # Pagina de cadastro
│   ├── __init__.py
│   ├── admin.py               # Registro dos modelos no painel admin
│   ├── apps.py                # Configuracao do app Django
│   ├── models.py              # Modelos: User, Category, Listing, Bid, Comment
│   ├── urls.py                # Rotas da aplicacao (13 endpoints)
│   ├── views.py               # Logica de negocio (10 views)
│   └── tests.py               # Testes (vazio por padrao)
│
├── db.sqlite3                 # Banco de dados SQLite
├── manage.py                  # CLI do Django
└── README.md                  # Este arquivo
```

---

## Modelos de Dados

### User
Herda de `AbstractUser` do Django. Ja possui username, email, password, etc.

### Category
| Campo | Tipo | Descricao |
|-------|------|-----------|
| `name` | CharField(64) | Nome da categoria |

### Listing
| Campo | Tipo | Descricao |
|-------|------|-----------|
| `title` | CharField(128) | Titulo do anuncio |
| `description` | TextField | Descricao detalhada |
| `starting_bid` | DecimalField(10,2) | Lance minimo inicial |
| `image_url` | URLField (opcional) | URL da imagem do produto |
| `category` | FK → Category (opcional) | Categoria do anuncio |
| `creator` | FK → User | Quem criou o anuncio |
| `active` | BooleanField | Se o leilao esta aberto |
| `watchers` | M2M → User | Usuarios que favoritaram |
| `created_at` | DateTimeField | Data de criacao |

**Metodo `current_price()`**: retorna o maior lance ou o `starting_bid` se ninguem deu lance.

### Bid
| Campo | Tipo | Descricao |
|-------|------|-----------|
| `amount` | DecimalField(10,2) | Valor do lance |
| `bidder` | FK → User | Quem deu o lance |
| `listing` | FK → Listing | Em qual anuncio |
| `created_at` | DateTimeField | Data do lance |

### Comment
| Campo | Tipo | Descricao |
|-------|------|-----------|
| `text` | TextField | Texto do comentario |
| `commenter` | FK → User | Quem comentou |
| `listing` | FK → Listing | Em qual anuncio |
| `created_at` | DateTimeField | Data do comentario |

---

## Rotas (URLs)

| Rota | View | Descricao |
|------|------|-----------|
| `/` | `index` | Anuncios ativos |
| `/login` | `login_view` | Login |
| `/logout` | `logout_view` | Logout |
| `/register` | `register` | Cadastro |
| `/create` | `create_listing` | Criar anuncio |
| `/listings/<id>` | `listing_page` | Detalhe do anuncio |
| `/listings/<id>/watchlist` | `toggle_watchlist` | Favoritar/desfavoritar |
| `/listings/<id>/bid` | `place_bid` | Dar lance |
| `/listings/<id>/close` | `close_auction` | Encerrar leilao |
| `/listings/<id>/comment` | `add_comment` | Comentar |
| `/watchlist` | `watchlist` | Meus favoritos |
| `/categories` | `categories` | Lista de categorias |
| `/categories/<id>` | `category_listings` | Anuncios por categoria |

---

## Tecnologias

- **Backend**: Python 3 + Django
- **Banco de dados**: SQLite3
- **Frontend**: HTML5 + CSS3 customizado (sem Bootstrap)
- **Fontes**: Google Fonts (Orbitron + Inter)
- **Tema**: Sistema claro/escuro com CSS custom properties + JavaScript

---

## Como Executar

```bash
# 1. Instalar dependencias
pip install django

# 2. Aplicar migracoes
python manage.py makemigrations auctions
python manage.py migrate

# 3. Criar superusuario (para acesso ao /admin/)
python manage.py createsuperuser

# 4. Iniciar servidor
python manage.py runserver

# 5. Acessar no navegador
# http://127.0.0.1:8000/
```

---

## Painel Admin

Acesse `http://127.0.0.1:8000/admin/` com o superusuario para visualizar, adicionar, editar e deletar:
- Usuarios
- Categorias
- Anuncios
- Lances
- Comentarios
