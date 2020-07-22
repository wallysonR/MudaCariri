# MudaCariri
MudaCariri - Aplicação para estimular a disseminação e plantio de mudas <br>
<strong>Contexto </strong>: Aplicação web utilizada para facilitar a comunicação entre usuários que querem doar(sementes,mudas, plantas ou frutos) e adotante.

### Como executar o projeto:

- Entre na pasta `project` na raiz do projeto e crie um virtualenv com o seguinte comando:

    ```python3 -m venv env```

- A seguir ative o virtualenv com o comando:

    ```source env/bin/activate```

- **(Opcional)** Atualize a versão do pip (gerernciador de pacotes do Python):

    ```pip install -U pip```

- Agora instale as dependências:

    ```pip install -r requirements.txt```

- Para as configurações do banco de dados, crie um arquivo nomeado `.env` no mesmo diretório onde se encontra o arquivo settings.py.
Neste arquivo coloque os seguintes dados:
    ```
    DB_NAME="NOME_DO_BANCO"
    DB_USER="USUARIO_LOGIN"
    DB_PASSWORD="SENHA_LOGIN"
    DB_HOST="localhost"
    DB_PORT="5432"
    ```

- lembre-se de mudar `NOME_DO_BANCO` para o nome do seu banco de dados, `USUARIO_LOGIN` para o seu usuário do postgres, `SENHA_LOGIN` para a senha do postgres.

- **Obs:** Esse tipo de arquivo é uma boa prática quando se tem dados sensíveis na sua aplicação, como logins de banco, tokens de acesso, etc. Nesse caso o arquivo `.env` não é enviado ao github, ficando somente na máquina do usuário e assim permitindo que cada pessoa que trabalha no projeto tenha suas próprias configurações. 