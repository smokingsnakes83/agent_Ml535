![Agent M|535](https://github.com/smokingsnakes83/agent_Ml535/blob/main/assets/asset1.png?raw=true)

## **Objetivo**:
Criar um chatbot que responde a perguntas do usuário sobre Mises e a Escola Austríaca de Economia, utilizando um modelo de linguagem de grandes dimensões.
### **Funcionalidades**:
**Histórico de conversas**: O código utiliza st.session_state para armazenar o histórico de mensagens, permitindo que o usuário visualize a conversa em tempo real.<br>
**Entrada de usuário**: O chatbot captura a entrada do usuário por meio de um campo de texto (st.chat_input).<br>
**Geração de resposta**: O código utiliza o modelo de linguagem genai.GenerativeModel para gerar uma resposta com base na consulta do usuário e em um contexto de dados fornecido.<br>
**Exibição de respostas**: O chatbot exibe as respostas geradas pelo modelo de linguagem na interface do usuário, simulando uma conversa natural.<br>
## **Bibliotecas**:
### **O Agent M|535 utiliza as seguintes bibliotecas**:<br>
**streamlit**: Para criar a interface web do chatbot.<br>
**google.generativeai**: Para a geração de texto com o modelo de linguagem gemini-1.5-pro-latest.<br>
### **Parâmetros**:
**df**: DataFrame contendo os dados relevantes sobre Mises e a Escola Austríaca de Economia.<br>
**gen_model**: Objeto genai.GenerativeModel configurado para o modelo gemini-1.5-pro-latest.<br>
**embed_model**: Modelo de embedding para processar a consulta do usuário e gerar um contexto de dados para o modelo de linguagem.<br>
**gen_config**: Configuração específica para o modelo de geração de texto.<br>
**safety_config**: Configurações de segurança para o modelo de linguagem.<br>
## **Funções**:
**chat_history(messages)**: Função responsável por exibir o histórico de mensagens da conversa.
### Parâmetros:
**messages**: Lista de dicionários, cada um representando uma mensagem com os campos role (identificação do emissor, "user" ou "assistant") e content (conteúdo da mensagem).<br>
**Retorno**: Sem retorno, apenas exibe o histórico de mensagens na interface.<br>
**input_user_query(user_query, df, gen_model, embed_model)**: Função responsável por processar a consulta do usuário, gerar uma resposta e retornar o texto da resposta.<br>
### Parâmetros:
**user_query**: Consulta do usuário.<br>
**df**: DataFrame com dados relevantes.<br>
**gen_model**: Modelo de linguagem.<br>
**embed_model**: Modelo de embedding.<br>
**Retorno**: Texto da resposta gerada pelo modelo de linguagem.<br>
## **Detalhes da implementação:**
O código inicializa o histórico de mensagens (st.session_state.messages).<br>
A função chat_history é chamada para exibir o histórico de mensagens atual.<br>
O código captura a consulta do usuário por meio de st.chat_input.<br>
A consulta é adicionada ao histórico de mensagens.<br>
A função input_user_query é chamada para processar a consulta, gerar a resposta e retornar o texto da resposta.<br>
A resposta é exibida na interface do usuário.<br>
A resposta é adicionada ao histórico de mensagens.
## **Exemplo de uso:**
![Agent M|535](https://github.com/smokingsnakes83/agent_Ml535/blob/main/assets/asset4.gif)
