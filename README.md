# Banco de Dados I

## 1º Trabalho

### Equipe

- José Ricardo Sampaio Coutinho II - 22052568
- Nasthya Barauna - 22050961
- Tedy Prist - 22050676

### Como executar

No diretório raiz desse projeto, execute o seguinte comando para criar um container docker com a imagem do postgres:

```bash
docker-compose up -d
```

Em seguida execute o seguinte comando para instalar as dependências do python:

```bash
pip install -r requirements.txt
```

#### Criando e populando as tabelas

Caso precise mudar os parâmtros para acesso ao banco de dados, basta alterar os campos no arquivo **.env**

O arquivo a ser executado para gerar e popular as tabelas do banco de dados chama-se **tp1_3.2.py** e é necessário passar como parâmetro de execução o nome do arquivo que será processado, da seguinte forma:

```bash
python3 scripts/tp1_3.2.py "scripts/resources/amazon-meta-test.txt"
```

#### Executando as consultas

Para executar todas as consultas, execute o arquivo que chama-se **tp1_3.3.py** . Algumas consultas recebem parâmetros como entrada, os quais podem ser modificados no arquivo **dashboard.py**

```bash
python3 scripts/tp1_3.3.py
```

### Observação

Foi adicionando um arquivo de teste chamado **amazon-meta-test.txt** apenas para facilitar o desenvolvimento rápido, porém ele conta com apenas uma fatia do arquivo original então os nem todas as consultas retornarão resultados completos devido a falta de dados.

O arquivo principal **amazon-meta.txt** não está versionado neste repositório devido ao seu extenso tamanho, para sua utilização basta adicioná-lo à pasta "resources" e executar o comando descrito anteriormente e os resultados serão completos
