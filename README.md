# BBB API

## Respostas do desafio

### 1 - Desenvolva uma API em Python, implementando um CRUD simples para receber inscrições do BBB 24.

- Para garantir a facilidade de instalação, incluí o arquivo [INSTALLATION.md](https://github.com/samueledson/bbb/blob/main/INSTALLATION.md) com os passos necessários. Sugiro fazer a construção da aplicação com o Docker.
- A ideia apresenta um cenário onde existe uma tabela para armazenar os dados dos candidatos, as inscrições para determinada temporada, as respostas do candidato em determinada inscrição e claro uma tabela que com as perguntas que podem ser classificadas por seção/assunto. Cada candidato pode realizar uma inscrição para uma temporada do programa. Na tabela de inscrição tem um status que pode controlar a estado da inscrição, como pendente, entregue, seletivas, etc. Na raiz desse repositório tem uma [imagem](https://github.com/samueledson/bbb/blob/main/diagrama-eer.png) com o diagrama com a modelagem do banco de dados.
- Nessa ideia o foco foi deixar o máximo de regras de negócio possível na responsabilidade da API. O uso de uma tabela de perguntas é um exemplo disso. Fica a cargo da API fornecer as perguntas a serem feitas, e caso uma pergunta seja desativa ou uma nova incluída, o front-end se adapta perfeitamente, assim como outras regras como a persistência de dados em uma nova temporada.
- Em algumas tabelas faço uso de campos do tipo Enum para que não fosse preciso a criação de muitas outras entidades para compor o cenário proposto.

### 2 - Supondo que seja necessário o desenvolvimento de um frontend para consumo da API desenvolvida anteriormente. Quais componentes você utilizaria e por quê?

- Utilizaria componentes para construir o formulário principal, como componente para botões, para campos de texto, data, seleção de opções, exibição de mensagem/avisos, etc. Também adotaria a metodologia de nomenclatura de classes CSS chamada BEM (Block Element Modifier) para tornar a estilização modular e aumentar a legibilidade do código.
- Adicionaria reatividade entre os elementos e componentes, poderia utilizar uma biblioteca como o React ou Web Components (até pela simplicidade das interações). No entanto, para este desafio, optei por utilizar o Angular, que é meu framework de frontend favorito e que tenho mais familiaridade, garantindo agilidade no desenvolvimento do desafio por estar mais fresco na minha memória. Em um cenário real, consideraria o uso do React ou Vue.js, de acordo com os requisitos as ferramentas que essas duas últimas possuem seria o suficiente.
- Foi desenvolvido o front-end pra esse desafio. A realização dessa parte foi importante pra mim até para provar o uso junto da API, ter uma visibilidade mais próxima da solução apresentada e também mostrar um pouco mais das minhas habilidades e competências. Apesar disso, a qualidade do código no front-end não foi uma preocupação para o momento e tempo, por gentileza, considere essa informação.

### 3 - Faça uma breve descrição das bibliotecas e frameworks utilizados (1 a 3 linhas), justificando o motivo de sua utilização.

- Para atender ao desafio, desenvolvi uma API em Python utilizando o framework assíncrono FastAPI, que permite alta performance e escalabilidade. O banco de dados MySQL foi escolhido por atender bem ao objetivo, e o ORM SQLAlchemy permitiu o gerenciamento dos dados de forma simples e com possibilidade de uso de outros bancos com sua rica abstração. A técnica de "soft delete" foi aplicada para desativação dos registros mantendo-os no banco. O FastAPI também gera automaticamente as documentações para o Swagger com o uso de decorators nas rotas implementadas, garantindo agilidade no desenvolvimento. Utilizei a biblioteca Pytest para realização dos testes.
- O código em Python pode parecer inconsistente. Há lugares com comentários, e outros não por exemplo. A intenção foi fazer o uso de boas práticas de desenvolvimento onde foi possível, devido ao tempo.

### 4 - O CRUD desenvolvido possui a melhor performance possível? Justifique sua resposta.

- Embora este desafio não tenha uso em ambiente de produção, desenvolvi o CRUD considerando algumas técnicas para garantir performance, como o uso do framework assíncrono FastAPI e a modelagem do banco de dados com índices que podem otimizar as execuções das queries de consulta. Validações na persistência dos dados também foram implementadas.
- Sem dúvida há espaço para muitas melhorias, principalmente pensando em performance. Em um cenário real, o que vejo até então seria o uso de uma estrutura Cloud, como GCP e AWS, que possibilita a elasticidade necessária para o uso do banco de dados, armazenamento dos arquivos (ex. o vídeo de inscrição) e também o gerenciamento da carga de trabalho com um possível aumento das requisições feitas para API sem comprometer a disponibilidade e desempenho. O uso de um serviço de cache e CDN para servir os arquivos estáticos e até mesmo para cachear os endpoints com poucas alterações, como o endpoint de perguntas por exemplo.
- O uso de um token de acesso para as requisições (como o JWT) seria essencial. A adição de um captcha e token CSRF, diminuiria a possibilidade de uso de bots e ataques mal intencionados ao enviar o formulário com os dados.

## Observações

- Desenvolvi o back-end e o front-end para o desafio.
- Na raiz desse repositório tem uma imagem com o diagrama de entidade relacionamento estendido.
- Qualquer dúvida ou problema estou a disposição.