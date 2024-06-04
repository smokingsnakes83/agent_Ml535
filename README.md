![Agent M|535](https://github.com/smokingsnakes83/agent_Ml535/blob/main/assets/asset1.png?raw=true)

## **O que é o Agent M|535**:
O agent M|535 é um chatbot que responde a perguntas do usuário sobre Mises e a Escola Austríaca de Economia, com a intenção de ajudar o usuário a entender a economia pela ótica da Escola Austríaca utilizando um modelo de linguagem de grandes dimensões.

## **Instalação**
### Pré-requisitos:
**Conta do Google Cloud**: Crie uma conta gratuita no Google Cloud https://cloud.google.com/ e habilite a API do Google Generative AI https://ai.google.dev/gemini-api.<br>
**Python**: Baixe e instale a versão mais recente do Python https://www.python.org/downloads/<br>
**Git**: Baixe e instale o Git https://git-scm.com/downloads<br><br>
### Instalar as dependências:
Abra o seu terminal e navegue para o diretório desejado para a instalação.<br>
Crie um ambiente virtual (opcional, mas recomendado) usando o seguinte comando:<br>
```bash
# Linux e Mac
python -m venv agent_mises 
source .venv/bin/activate
```
```powershell
# Windows
python -m venv agent_mises
agent_mises\Scripts\activate
```
Instale as dependências definidas no arquivo requirements.txt usando o seguinte comando:<br>
```bash
pip install -r requirements.txt
```
## Configurar a API Key do Google Generative AI:<br>
Acesse a API do Google Generative AI.<br>
Salve a chave de API em um arquivo .env na raiz do seu projeto. O arquivo deve ter a seguinte estrutura:<br>
```.env
API_KEY=sua_chave_api
```
Clone o repositório do GitHub usando o seguinte comando:

```bash
 git clone https://github.com/smokingsnakes83/agent_Ml535.git agent_MI535
```
## Executar o aplicativo:
Navegue para o diretório do projeto:<br>
```bash
cd agent_MI535
```
### Execute o aplicativo Streamlit com o seguinte comando:
```bash
streamlit run agent_mises.py
```
## Acessar o aplicativo:
O aplicativo Streamlit será aberto no seu navegador padrão. A URL será similar a http://localhost:8501/.

## **Exemplo de uso:**
![Agent M|535](https://github.com/smokingsnakes83/agent_Ml535/blob/main/assets/asset4.gif)
