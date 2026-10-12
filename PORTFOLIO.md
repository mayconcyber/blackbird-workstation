# BLACKBIRD Workstation — Network Inspector

**Versão:** 0.1.0 · **Plataforma:** Windows · **Tecnologias:** Python, Tkinter, Windows PowerShell, unittest.

## Problema e solução

Para estudar redes, é útil relacionar endereços e portas aos programas executados no computador. O BLACKBIRD reúne interfaces, configuração IP e conexões TCP em uma interface desktop com filtro e exportação de relatórios.

## Decisões de engenharia

- Biblioteca padrão do Python, sem dependências externas, para simplificar instalação e manutenção em um notebook de 8 GB.
- Separação entre interface e coleta, permitindo testar parsing e falhas sem depender da rede real.
- Thread de coleta e fila de resultados para manter as operações Tkinter na thread principal.
- Consulta local somente leitura com script fixo, atualização manual e limite de tempo.

## Evidências

Seis testes automatizados cobrem formato de dados, filtro, timeout e erros do coletor. Um teste de interface com dados sintéticos verifica tabelas, rótulos e contagens. No Windows do usuário, foram confirmados consulta real, detecção de um servidor em loopback na porta 8765, desaparecimento do listener após encerramento e correspondência do PID do OneDrive com o Gerenciador de Tarefas. A exportação foi realizada; o arquivo pessoal não faz parte do projeto público.

O consumo de RAM ainda precisa ser medido. Esta versão não determina se uma conexão é maliciosa: mostra dados para inspeção e aprendizado.

## Apresentação no GitHub

Nome sugerido do repositório: `blackbird-workstation`.

Descrição sugerida: Aplicativo desktop em Python para inspecionar a rede local no Windows, com conexões TCP, identificação de processos e exportação JSON.

Publique apenas o código, testes e documentação deste projeto. Use uma imagem com dados sintéticos para a apresentação. Revise imagens e relatórios pessoais antes de incluí-los. A publicação e a criação do repositório ainda não foram realizadas.

Este projeto foi desenvolvido com assistência do Codex e validado pelo usuário em seu ambiente Windows. A compreensão e evolução do código fazem parte da trilha de formação.
