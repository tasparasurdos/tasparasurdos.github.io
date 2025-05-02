# Catálogo de Tecnologias Assistivas para Surdos

Este projeto é um produto do Mestrado Profissional em Computação Aplicada da Universidade Federal de Mato Grosso do Sul (UFMS). Ele consolida três componentes que geram diferentes formatos de saída a partir de uma fonte de dados comum (planilhas CSV hospedadas no Google Sheets) e imagens centralizadas. Os componentes são:

1. **Site Estático**: Um site HTML com páginas para tecnologias assistivas, recursos pedagógicos e informações gerais.
2. **API**: Arquivos JSON que fornecem dados estruturados para integração com outras aplicações.
3. **Ebook**: Um catálogo em PDF com detalhes das tecnologias assistivas e recursos pedagógicos interessantes.

Os resultados são gerados no diretório `docs/`, que serve como o ponto de publicação para acesso público via internet.

## Estrutura do Projeto

```
.
├── api/
│   ├── api.py              # Script para gerar a API JSON
│   └── index.html          # Documentação da API
├── docs/                   # Diretório de saída para todos os resultados
├── ebook/
│   ├── conteudos/          # Templates HTML e recursos para o ebook
│   ├── ebook.py            # Script para gerar o ebook PDF
│   └── fontes/             # Fontes usadas no ebook
├── imagens/                # Imagens compartilhadas entre os componentes
├── website/
│   ├── assets/             # Arquivos estáticos (CSS, JS, imagens específicas)
│   ├── templates/          # Templates HTML para o site
│   └── website.py          # Script para gerar o site estático
├── Dockerfile              # Configuração do contêiner Docker
├── docker-compose.yml      # Configuração do serviço Docker Compose
├── main.py                 # Script interativo para executar os componentes
├── README.md               # Este arquivo
└── requirements.txt        # Dependências Python
```

### Estrutura de Saída (`docs/`)

```
docs/
├── imagens/                # Imagens compartilhadas
├── api/                    # Arquivos JSON e documentação da API
├── ebook/                  # Ebook em PDF
├── assets/                 # Arquivos estáticos do site
├── contato.html            # Página de contato
├── equipe.html             # Página da equipe
├── index.html              # Página inicial do site
├── mapa.html               # Mapa do site
├── recursos.html           # Página de recursos
├── sobre.html              # Página sobre
└── tecnologias/            # Páginas individuais das tecnologias
```

## Pré-requisitos

- **Docker** e **Docker Compose** instalados:
  - [Instalar Docker](https://docs.docker.com/get-docker/)
  - [Instalar Docker Compose](https://docs.docker.com/compose/install/)
- **Acesso à internet**: Para baixar os dados das planilhas do Google Sheets.

Alternativamente, para execução sem Docker:
- **Python 3.8+**
- **wkhtmltopdf**: Necessário para gerar o ebook. Instale conforme seu sistema operacional:
  - Linux: `sudo apt-get install wkhtmltopdf`
  - Windows/Mac: Baixe em [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)

## Instalação e Execução com Docker

1. **Clone o repositório**:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
   ```

2. **Construa e inicie o contêiner**:
   ```bash
   docker-compose up --build
   ```

3. **Acesse o contêiner**:
   ```bash
   docker exec -it tasparasurdos bash
   ```

4. **Execute o projeto** dentro do contêiner:
   ```bash
   python main.py
   ```
   - **Opções**:
     - Limpar o diretório `docs/` antes da geração (opcional).
     - Escolher o que gerar: API, Ebook, Site ou Todos.
   - **Resultado**: Os arquivos são gerados em `docs/`, e a pasta `imagens/` é copiada para `docs/imagens/`.

5. **Acesse os resultados**:
   - Os arquivos gerados estão em `./docs/` no diretório local (mapeado via volume no `docker-compose.yml`).
   - Para parar o contêiner:
     ```bash
     docker-compose down
     ```

## Instalação e Execução sem Docker

1. **Clone o repositório**:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
   ```

2. **Crie um ambiente virtual** (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verifique o wkhtmltopdf**:
   ```bash
   wkhtmltopdf --version
   ```
   Se não estiver instalado, siga as instruções de instalação acima.

5. **Execute o projeto**:
   ```bash
   python main.py
   ```
   - Escolha o que gerar: API, Ebook, Site ou Todos.
   - Os resultados são gerados em `docs/`.

### Execução de Componentes Isoladamente

Cada componente pode ser executado diretamente:

- **Gerar a API**:
  ```bash
  python api/api.py
  ```
- **Gerar o Ebook**:
  ```bash
  python ebook/ebook.py
  ```
- **Gerar o Site**:
  ```bash
  python website/website.py
  ```

**Nota**: Executar isoladamente não copia a pasta `imagens/` para `docs/imagens/`. Use `main.py` para uma geração completa.

## Fontes de Dados

Os dados são obtidos de duas planilhas no Google Sheets:
- **Tecnologias**: [Link](https://docs.google.com/spreadsheets/d/1g-zamZFp5FHTGxZOA0vT3ULXjwROhWS0mz0_K1xTvXc)
- **Recursos**: [Link](https://docs.google.com/spreadsheets/d/1lePYinFlYePVYPwwUqy1Xa1r1FF_l3vaAkRxntSvWq4)

As URLs estão configuradas em `main.py` e podem ser usadas como padrão pelos scripts individuais.

## Contexto Acadêmico

Este projeto foi desenvolvido como parte do Mestrado Profissional em Computação Aplicada da Universidade Federal de Mato Grosso do Sul (UFMS). Ele visa fornecer recursos acessíveis para promover a comunicação, a aprendizagem e a acessibilidade de estudantes surdos no contexto escolar.

## Contribuição

1. Fork o repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`).
4. Push para a branch (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

## Contato

Para dúvidas ou sugestões, entre em contato via [paulovander -at- gmail.com](mailto:paulovander@paulovander.com).