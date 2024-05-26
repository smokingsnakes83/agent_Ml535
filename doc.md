# **Documentação Detalhada**
## **embed_fn()**
## **Função que Gera Embeddings para os Documentos**
### **Função embed_fn:**<br>
A função **embed_fn()** recebe o título e o texto de um documento como entrada.
Ela usa a função genai.embed_content (assumindo que genai é uma biblioteca ou API de embedding) para gerar um vetor de embedding que representa o documento.

O argumento **model** especifica o modelo de embedding a ser usado.

O argumento **task_type='retrieval_document'** indica que o embedding será usado para tarefas de recuperação de documentos.
A função retorna o vetor de embedding do documento.

###**Aplicação da função ao dataframe:**<br>
A linha **df['Embeddings'] = df.apply(lambda row: embed_fn(row['Titulo'], row['Conteudo']), axis=1)** aplica a função embed_fn a cada linha do dataframe df.<br><br>
**df.apply(..., axis=1)** aplica a função a cada linha (eixo 1).<br><br>
A função **lambda lambda row: embed_fn(row['Titulo'], row['Conteudo'])** extrai o título **(row['Titulo'])** e o conteúdo **(row['Conteudo'])** de cada linha e os passa para a função **embed_fn**.<br><br>
O resultado da função **embed_fn (o vetor de embedding)** é armazenado na nova coluna **'Embeddings'** do dataframe.
###**Finalidade:**
Este código gera embeddings para cada documento (representado por título e conteúdo) no dataframe, armazenando os embeddings na coluna 'Embeddings'. Isso permite que os documentos sejam comparados semanticamente usando seus embeddings, por exemplo, para realizar buscas por similaridade ou agrupamento.

## **embed_query()**
## **Função que gera embeddings das consultas**
### **Objetivo:**<br>
A função **embed_query()** visa recuperar a informação mais relevante de um conjunto de dados estruturado com base na similaridade semântica com uma consulta fornecida pelo usuário.
### **Funcionamento:**<br>
1. **embed_query():** A função gera um embedding da consulta usando a função *genai.embed_content*.<br>
2. **similarity**: Em seguida, a função calcula a similaridade do cosseno entre o embedding da consulta e os embeddings armazenados no dataframe base.
3. **Identificação da informação mais semelhante:** O índice da informação com maior similaridade é identificado.
Verificação da similaridade: A similaridade é comparada com o limite definido.<br>
4. **Retorno da informação:** Se a similaridade for maior ou igual ao limite, a função retorna a informação correspondente do dataframe.
5. **Mensagem de erro:** Se a similaridade for menor que o limite, a função retorna uma mensagem informando que não foi possível encontrar uma resposta adequada.
### **Utilização:**
A função recebe a consulta do usuário (*query*), o dataframe contendo os embeddings e as informações (*base*), o modelo de embedding (*model*), e o limite de similaridade (*limit*).<br>
A função retorna uma tupla contendo a informação correspondente ou a mensagem de erro, juntamente com o valor da similaridade do cosseno.
### **Observações:**
O código assume que a biblioteca genai está disponível e configurada.
O dataframe base precisa conter as colunas 'Embeddings' e 'Conteudo'.
O limite de similaridade (*limit*) pode ser ajustado para controlar a sensibilidade da busca.
# **Configuração de Parâmentros**
## **gen_config:**
**candidate_count:** Define o número de candidatos de texto a serem gerados para cada solicitação. Neste caso, será gerado apenas 1 candidato.<br>
**temperature:** Controla a aleatoriedade da geração de texto. Um valor mais alto (próximo de 1) gera resultados mais criativos e imprevisíveis, enquanto um valor mais baixo (próximo de 0) gera resultados mais previsíveis e semelhantes ao texto de entrada. Neste caso, a temperatura está definida como 0.3, o que indica um nível moderado de aleatoriedade.
**top_k e top_p:** (Não definidos neste código) Esses parâmetros são usados para limitar o vocabulário do modelo durante a geração de texto. O top_k seleciona os k tokens mais prováveis para serem considerados, enquanto o top_p seleciona os tokens cuja probabilidade acumulada atinge o valor p.<br>
## **safety_config:**
Este dicionário define os níveis de bloqueio para diferentes tipos de conteúdo prejudicial, com os seguintes parâmetros:<br><br>
**harassment:** Bloqueia conteúdo de assédio.<br>
**hate:** Bloqueia conteúdo de ódio.<br>
**sexual:** Bloqueia conteúdo de natureza sexual.<br>
**dangerous:** Bloqueia conteúdo perigoso ou que promova ações perigosas.<br><br>
Neste caso, todos os parâmetros estão definidos como block_none, o que significa que nenhum tipo de conteúdo prejudicial será bloqueado.<br>
Nota: A configuração da segurança pode variar dependendo da plataforma ou ferramenta que utiliza este código.

# **Agent M|535**
## **Objetivo**:
Criar um chatbot que responde a perguntas do usuário sobre Mises e a Escola Austríaca de Economia, utilizando um modelo de linguagem de grandes dimensões.
### **Funcionalidades**:
**Histórico de conversas**: O código utiliza st.session_state para armazenar o histórico de mensagens, permitindo que o usuário visualize a conversa em tempo real.<br>
**Entrada de usuário**: O chatbot captura a entrada do usuário por meio de um campo de texto (st.chat_input).<br>
**Geração de resposta**: O código utiliza o modelo de linguagem genai.GenerativeModel para gerar uma resposta com base na consulta do usuário e em um contexto de dados fornecido.<br>
**Exibição de respostas**: O chatbot exibe as respostas geradas pelo modelo de linguagem na interface do usuário, simulando uma conversa natural.<br>
## **Utilização**:
**O código utiliza as seguintes bibliotecas**:<br>
**streamlit**: Para criar a interface web do chatbot.
genai: Para a geração de texto com o modelo de linguagem gemini-1.5-pro-latest.<br>
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
>>> You: O que é a Escola Austríaca de Economia?<br><br>
>>> Agent M|535: A Escola Austríaca de Economia é uma escola de pensamento econômico que se concentra no individualismo metodológico, na ação humana e nos mercados livres.


