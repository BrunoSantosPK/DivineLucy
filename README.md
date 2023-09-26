# Lucy Gestão Pessoal

Este projeto representa uma contribuição para a democratização do controle financeiro para todas as pessoas. É estruturado sobre uma forte base teórica de contabilidade, adaptando sua interface para ser simples de utilização para todo o público, do mais especialista ao mais leigo.

O projeto está concluído em sua primeira versão, estando no aguardo de liberação de hospedagem para publicação *online*.

## Ambição

Com o tempo, Lucy será capaz de sugerir para cada pessoa importantes informações sobre a saúde financeira. Mais poderoso que uma planilha e mais amigável que um ERP, as dicas serão formas de auxiliar cada usuário no processo de entendimento do próprio comportamento

## Funcionalidades Existentes

Atualmente as funcionalidades existentes são:

1. Controle de carteiras.
2. Gestão de tags de classificação para qualificar uma meta ou um registro.
3. Criação de metas para gastos e acompanhamento de execução.
4. Registro de movimentações finaneiras.

## Aspectos Técnicos

O sistema é construído com Python, tendo como framework full-stack o Flask. Para armazenamento de dados é utilizado o PostgreSQL e o log de utilização das funcionalidades são registrados em MongoDB.

Este repositório conta com todo o código fonte, com exceção do arquivo *.env* com as credenciais de conexão. Para os que desejarem copiar e executar o projeto localmente ou em servidor próprio, o arquivo *.env.example* possui o esqueleto de todas as credenciais necessárias, basta preencher com as próprias.

Para gestão de autenticação é utilizado o JWT armazenado via cookie, permitindo uma execução em pilha das atividades da rota, sempre verificando o JWT do usuário logado. Ja a autorização é verificada a nível de política nas atividades em que são necessárias, garantindo que um usuário não acesse ou modifique dados de outro.

O armazenamento de senhas é feito por meio de criptografia, de modo que o banco de dados não possui acesso à senha do usuário. Um sistema próprio para recuperação, que utiliza o e-mail cadastrado é utilizado em casos de esquecimento de senha.