# Arquitetura Futura

## Front-end

Em uma evolução futura, a aplicação poderia possuir um front-end separado consumindo a API.

O front-end seria responsável pela experiência do usuário, navegação e exibição das funcionalidades conforme as permissões do usuário.

Com a autenticação corporativa, o front-end também participaria do fluxo de login e manutenção da sessão do usuário.

## Autenticação corporativa

A aplicação poderia integrar com o provedor de identidade corporativo utilizando **OAuth 2.0 / OpenID Connect (OIDC)**, como Microsoft Entra ID.

## Controle de permissões

Após a autenticação, seria implementado controle de acesso baseado em perfis e permissões.

Exemplo:

- **Solicitante:** cria e consulta suas solicitações.
- **Aprovador:** aprova ou rejeita solicitações.
- **Administrador:** possui acesso administrativo.

## Auditoria

O histórico atual poderia evoluir para uma auditoria completa, registrando:

- usuário aprovador;
- data e hora da criação;
- ação realizada;

