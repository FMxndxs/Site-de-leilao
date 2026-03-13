# Deploy no Render

## Passo a passo

### 1. Preparar o repositório
- Faça commit e push das alterações para o GitHub (branch `web50/projects/2020/x/commerce` ou `main`)

### 2. Criar conta no Render
- Acesse [render.com](https://render.com)
- Clique em **Get Started for Free**
- Faça login com sua conta **GitHub**

### 3. Criar o Banco de Dados
1. No dashboard do Render, clique em **New +** → **PostgreSQL**
2. Dê um nome (ex: `commerce-db`)
3. Clique em **Create Database**
4. Após criar, copie a **Internal Database URL** (ou External, se for conectar de fora)

### 4. Criar o Web Service
1. Clique em **New +** → **Web Service**
2. Conecte o repositório do GitHub (autorize se pedir)
3. Selecione o repositório **me50/FMxndxs** (ou o seu)
4. Configure:

| Campo | Valor |
|-------|-------|
| **Name** | commerce (ou outro nome) |
| **Region** | Ohio (ou mais próximo) |
| **Branch** | web50/projects/2020/x/commerce ou main |
| **Root Directory** | (deixe vazio) |
| **Runtime** | Python 3 |
| **Build Command** | `./build.sh` ou `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `python -m gunicorn commerce.wsgi:application --bind 0.0.0.0:$PORT` |

### 5. Variáveis de Ambiente
Na aba **Environment**, adicione:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Cole a Internal Database URL do PostgreSQL que você criou |
| `SECRET_KEY` | Gere uma chave aleatória (ex: `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DEBUG` | `False` |

### 6. Start Command (**obrigatório** – sem isso o site não carrega!)
O app **precisa** escutar na porta que o Render define. No Render Dashboard → seu serviço → **Settings** → **Start Command**, use **exatamente** uma destas opções:

```
python -m gunicorn commerce.wsgi:application --bind 0.0.0.0:$PORT
```

**OU** (alternativa via script):

```
bash start.sh
```

### 7. Deploy
- Clique em **Create Web Service**
- Aguarde o build terminar (pode levar 2–5 minutos)
- Seu site estará em `https://seu-app.onrender.com`

### 8. Após o primeiro deploy

**Superusuário (admin) – plano gratuito sem Shell:**  
Vá em **Environment** → **Add Environment Variable** e adicione:

| Key | Value |
|-----|-------|
| `DJANGO_SUPERUSER_USERNAME` | admin (ou outro usuário) |
| `DJANGO_SUPERUSER_EMAIL` | admin@exemplo.com |
| `DJANGO_SUPERUSER_PASSWORD` | Senha segura para o admin |

Depois, clique em **Manual Deploy** → **Deploy latest commit**. O superusuário será criado automaticamente no próximo build. Acesse `https://seu-app.onrender.com/admin/` e faça login.

**Plano pago (com Shell):** Vá em **Shell** e execute `python manage.py createsuperuser`.

**Categorias:** As categorias iniciais (Eletrônicos, Moda, Esportes, etc.) são criadas automaticamente pela migração. Para criar novas categorias, use o **Admin** em `/admin/` → **Categorias** → **Adicionar**.

---

## Observações
- O app entra em **sleep** após ~15 min sem visitas (plano gratuito)
- A primeira visita após dormir pode levar ~30 segundos para carregar
- Para adicionar dados iniciais, use o admin ou o Django shell no Render
