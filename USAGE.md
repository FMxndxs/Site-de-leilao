# Guia de Uso — Commerce

Este documento explica como utilizar todas as funcionalidades do site de leiloes.

---

## 1. Cadastro e Login

### Criar uma conta
1. Clique em **Cadastrar** na barra de navegacao.
2. Preencha: usuario, e-mail, senha e confirmacao de senha.
3. Clique em **Cadastrar**. Voce sera logado automaticamente.

### Fazer login
1. Clique em **Entrar** na barra de navegacao.
2. Informe usuario e senha.
3. Clique em **Entrar**.

### Sair
- Clique em **Sair** na barra de navegacao. Voce sera redirecionado para a pagina inicial.

---

## 2. Navegacao

### Barra de navegacao
A barra no topo do site contem:
- **Leiloes** (logo) — volta para a pagina inicial.
- **Anuncios** — lista todos os anuncios ativos.
- **Categorias** — lista todas as categorias disponiveis.
- **Favoritos** — mostra seus anuncios favoritos (com badge de contagem).
- **+ Criar** — abre o formulario para criar um novo anuncio.
- **Sair** — encerra a sessao.
- **Botao de tema** (sol/lua) — alterna entre modo claro e escuro.

> Os links Favoritos, + Criar e Sair so aparecem para usuarios logados.
> Para visitantes, aparecem Entrar e Cadastrar.

### Alternancia de tema
- Clique no icone de **lua** (modo claro) ou **sol** (modo escuro) no canto direito da navbar.
- A preferencia e salva no navegador e persiste entre visitas.

---

## 3. Anuncios Ativos (Pagina Inicial)

A pagina inicial exibe todos os leiloes ativos em um **grid de cards**.

Cada card mostra:
- **Imagem** do produto (ou placeholder "SEM IMAGEM").
- **Tag de categoria** no canto superior direito.
- **Titulo** do anuncio (clicavel).
- **Descricao** resumida (primeiras 20 palavras).
- **Preco atual** (maior lance ou lance inicial).
- **Data de criacao**.

Clique em qualquer card para ver os detalhes completos.

---

## 4. Pagina do Anuncio (Detalhe)

Ao clicar em um anuncio, voce ve:

### Informacoes exibidas
- Imagem em tamanho grande.
- Titulo + badge de status (**Ativo** ou **Encerrado**).
- Preco atual em destaque.
- Numero de lances (e se o seu e o maior).
- Descricao completa.
- Metadados: quem criou, categoria e data.

### Acoes disponiveis (usuario logado)

#### Favoritos
- **Adicionar aos Favoritos** — salva o anuncio na sua lista.
- **Remover dos Favoritos** — remove da lista.

#### Dar Lance
1. Digite o valor no campo "Seu lance...".
2. Clique em **Dar Lance**.
3. **Regras**:
   - Se nao ha lances, o valor deve ser **>=** ao lance inicial.
   - Se ja ha lances, o valor deve ser **>** que o maior lance atual.
   - Se o lance nao atender os criterios, uma mensagem de erro e exibida.

#### Encerrar Leilao
- Aparece **apenas para o criador** do anuncio.
- Clique em **Encerrar Leilao** para fechar.
- O maior lance no momento vence o leilao.
- O vencedor vera a mensagem: "Parabens! Voce venceu este leilao."

#### Comentar
1. Escreva seu comentario na caixa de texto.
2. Clique em **Comentar**.
3. O comentario aparece na lista abaixo com seu nome, avatar e data.

---

## 5. Meus Favoritos

- Acesse clicando em **Favoritos** na navbar.
- Exibe todos os anuncios que voce adicionou aos favoritos.
- A badge na navbar mostra quantos itens voce tem.
- Clique em qualquer card para ir ao detalhe e, se quiser, remover dos favoritos.

---

## 6. Categorias

- Acesse clicando em **Categorias** na navbar.
- Cada categoria e exibida como um card com icone emoji.
- Categorias disponiveis: Moda, Brinquedos, Eletronicos, Casa, Esportes, Livros, Outros.
- Clique em uma categoria para ver apenas os anuncios ativos dela.

---

## 7. Criar Anuncio

1. Clique em **+ Criar** na navbar (requer login).
2. Preencha o formulario:
   - **Titulo** (obrigatorio) — nome do produto.
   - **Descricao** (obrigatorio) — detalhes sobre o item.
   - **Lance Inicial** (obrigatorio) — valor minimo em R$.
   - **URL da Imagem** (opcional) — link direto para uma foto do produto.
   - **Categoria** (opcional) — selecione da lista.
3. Clique em **Criar Anuncio**.
4. Voce sera redirecionado para a pagina do novo anuncio.

---

## 8. Painel Administrativo

- Acesse `http://127.0.0.1:8000/admin/` com um superusuario.
- Funcionalidades:
  - **Usuarios**: ver, criar, editar e deletar contas.
  - **Categorias**: gerenciar categorias disponiveis.
  - **Anuncios**: ver todos os anuncios, filtrar por status (ativo/encerrado) e categoria.
  - **Lances**: ver historico de lances com usuario, anuncio e valor.
  - **Comentarios**: moderar comentarios.

---

## Usuarios de Teste

| Usuario | Senha | Perfil |
|---------|-------|--------|
| `admin` | `admin1234` | Superusuario (acesso ao /admin/) |
| `hermione` | `pass1234` | Usuario comum |
| `harry` | `pass1234` | Usuario comum |
| `ron` | `pass1234` | Usuario comum |
