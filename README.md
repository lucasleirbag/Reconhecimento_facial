# Reconhecimento Facial

Este projeto é um sistema de reconhecimento facial que usa o OpenCV e o Python. O sistema pode ser usado para cadastrar novos usuários, treinar o modelo e reconhecer rostos em tempo real.

## Como usar

Para usar o sistema, siga estas etapas:

1. Crie um banco de dados SQLite chamado `usuarios.db`.
2. Crie uma tabela chamada `usuarios` no banco de dados.
3. Adicione as seguintes colunas à tabela `usuarios`:
    * `id` (chave primária)
    * `nome` (texto)
    * `cpf` (texto)
4. Crie um diretório chamado `USUARIO`.
5. Crie um diretório para cada usuário no diretório `USUARIO`.
6. Salve as imagens dos rostos dos usuários nos diretórios dos usuários.
7. Treine o modelo usando o script `trainData.py`.
8. Execute o script `main.py` para iniciar o sistema de reconhecimento facial.

## Recursos

O sistema de reconhecimento facial possui os seguintes recursos:

* Cadastro de novos usuários
* Treinamento do modelo
* Reconhecimento de rostos em tempo real
* Alarme sonoro quando um rosto desconhecido é detectado

## Problemas conhecidos

O sistema de reconhecimento facial possui os seguintes problemas conhecidos:

* O sistema pode não funcionar corretamente se as imagens dos rostos dos usuários não forem de alta qualidade.
* O sistema pode não funcionar corretamente se os usuários estiverem usando óculos ou chapéus.
* O sistema pode não funcionar corretamente se os usuários estiverem em movimento.

## Licença

Este projeto está licenciado sob a licença MIT.
