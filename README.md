# mise. — cozinhe com o que você já tem

Aplicativo web de receitas por ingredientes e tempo disponível, feito com Streamlit.

## Rodar no computador

1. Instale Python 3.10 ou superior.
2. Extraia esta pasta.
3. Abra o terminal dentro da pasta `mise_app`.
4. Execute:

   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

5. O Streamlit abrirá o app no navegador.

## Publicar gratuitamente no Streamlit Community Cloud

Você precisará de uma conta GitHub.

1. Entre em https://github.com e crie uma conta, se ainda não tiver.
2. Crie um repositório novo chamado `mise-app` (pode ser público).
3. Envie todos os arquivos desta pasta para a raiz do repositório, incluindo `app.py`, `requirements.txt`, `.gitignore` e a pasta `.streamlit`.
4. Acesse https://share.streamlit.io/ e entre com sua conta GitHub.
5. Clique em **Create app**.
6. Escolha o repositório `mise-app`, a branch `main` e o arquivo principal `app.py`.
7. Clique em **Deploy**. Aguarde a instalação das dependências.

O Streamlit fornecerá um endereço público para abrir o aplicativo.

## O que funciona nesta versão

- Inclusão manual de ingredientes.
- Atalhos de ingredientes de exemplo.
- Seleção do tempo disponível.
- Sugestões baseadas em uma pequena coleção de receitas e correspondência de ingredientes.
- Visualização do passo a passo.

## Limitação atual

Esta versão ainda não chama um modelo de IA. As receitas são escolhidas a partir de uma base local de demonstração. Para gerar receitas novas dinamicamente, será necessário conectar uma API de IA (por exemplo, usando uma chave própria guardada nos Secrets do Streamlit). Não coloque chaves ou senhas diretamente no código ou no GitHub.

## Próximas melhorias recomendadas

1. Conectar uma API de IA para gerar receitas sob demanda.
2. Adicionar filtros de restrições e preferências alimentares.
3. Melhorar a correspondência de ingredientes e substituições.
4. Validar tempos e quantidades das receitas geradas.
