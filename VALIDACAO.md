# Validação da primeira entrega

## Confirmações no Windows do usuário

Durante a orientação, o usuário confirmou a consulta real, as linhas TCP, a porta 8765 em Listen após iniciar um servidor em 127.0.0.1 e o desaparecimento após Ctrl+C. Também confirmou o PID do OneDrive no Gerenciador de Tarefas e realizou a exportação JSON. São confirmações manuais do usuário, posteriores às limitações do ambiente do agente descritas abaixo. A versão com os novos cabeçalhos e resumo ainda deve ser reaberta no notebook para conferência visual.

- Seis testes automatizados passaram: formato/BOM, resposta inválida, filtro, timeout, erro de consulta e invocação fixa do coletor.
- Smoke test de Tkinter passou com dados sintéticos: criação da janela oculta, inserção de dados nas tabelas e filtro que elimina linhas. Não foi feita revisão visual da janela em tela.
- A coleta real não foi validada com sucesso neste ambiente: a primeira tentativa encontrou bloqueio CIM; a repetição fora do ambiente restrito excedeu o limite de 30 segundos. O aplicativo trata ambas as falhas com mensagem e preserva dados anteriores.
- Consumo de RAM não medido. A arquitetura evita dependências externas e coleta contínua, mas isso não garante uma quantidade específica de memória.

Execute o roteiro do README no Windows para confirmar a integração local. Se ocorrer o mesmo erro, execute `Get-NetIPConfiguration` e `Get-NetTCPConnection` separadamente no PowerShell e identifique qual consulta falha ou demora. Não altere políticas de segurança nem eleve a aplicação automaticamente. O coletor pode precisar de adaptação ao ambiente se esses comandos não estiverem disponíveis à conta atual.
