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
| **Start Command** | `gunicorn commerce.wsgi:application` |

### 5. Variáveis de Ambiente
Na aba **Environment**, adicione:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Cole a Internal Database URL do PostgreSQL que você criou |
| `SECRET_KEY` | Gere uma chave aleatória (ex: `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DEBUG` | `False` |

### 6. Deploy
- Clique em **Create Web Service**
- Aguarde o build terminar (pode levar 2–5 minutos)
- Seu site estará em `https://seu-app.onrender.com`

### 7. Criar superusuário (admin)
Após o primeiro deploy, vá em **Shell** no seu Web Service no Render e execute:

```bash
python manage.py createsuperuser
```

Informe usuário, e-mail e senha. Depois acesse `https://seu-app.onrender.com/admin/` para fazer login.

---

## Observações
- O app entra em **sleep** após ~15 min sem visitas (plano gratuito)
- A primeira visita após dormir pode levar ~30 segundos para carregar
- Para adicionar dados iniciais, use o admin ou o Django shell no Render
