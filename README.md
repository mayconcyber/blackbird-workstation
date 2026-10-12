# BLACKBIRD Workstation

**Versão 0.1.0** · Windows · Python/Tkinter · Sem dependências externas

[Apresentação para o portfólio](PORTFOLIO.md) · [Histórico de versões](CHANGELOG.md) · [Validação](VALIDACAO.md)

Aplicativo desktop para Windows 11, em Python e Tkinter, com Network Inspector local. Primeira entrega funcional; os módulos de programação, Linux e laboratórios ofensivos/defensivos estão planejados, ainda não implementados.

## Abrir no VS Code

1. Abra esta pasta `BLACKBIRD` como pasta de trabalho no VS Code.
2. Instale Python 3.12 ou superior pelo instalador oficial: https://www.python.org/downloads/windows/ . Inclua Tcl/Tk. Se `python --version` abrir a loja ou falhar, selecione o executável instalado, em vez do alias WindowsApps.
3. Instale a extensão Python da Microsoft no VS Code e use **Python: Select Interpreter** para selecionar esse Python.
4. No terminal da pasta, execute:

```powershell
python -m tkinter
python -m blackbird
```

O primeiro comando verifica se Tkinter está disponível. O segundo abre o aplicativo. Também há uma configuração de depuração: selecione **BLACKBIRD Workstation** e pressione F5, com a extensão Python Debugger instalada.

Não há pacotes externos a instalar. Use uma conta comum do Windows. A aplicação consulta os dados visíveis à conta atual; uma falha de permissão aparece na interface.

## O primeiro módulo

- Interfaces: nome, IPv4, IPv6, gateway IPv4 e DNS.
- Conexões TCP: endereços, portas, estado, PID e nome do processo quando disponível.
- Filtro por qualquer valor da conexão e exportação do retrato completo em JSON.
- Cabeçalhos em português, contagem de resultados e resumo da última consulta: interfaces, registros TCP e números de porta distintos em escuta.
- Aba de exercícios e mensagens de erro; dados anteriores são preservados se a atualização falhar.

A consulta ocorre somente ao clicar. Não há captura de pacotes, varredura de rede, teste de portas remotas, alteração de firewall ou execução de comandos digitados pelo usuário. O filtro não gera tráfego. Um processo pode encerrar durante a consulta e aparecer sem nome. Gateway IPv6, UDP e histórico ainda não são exibidos.

## Arquitetura e orçamento para 8 GB

`blackbird/ui.py` apresenta dados e exercícios. `blackbird/network.py` consulta o Windows PowerShell com um script fixo e normaliza o JSON. `blackbird/__main__.py` inicia a interface ou uma consulta sem janela. `tests/` valida parsing, filtro e tratamento de falhas.

Uma única coleta roda por vez em uma thread; uma fila leva o resultado à thread principal do Tkinter. A consulta tem limite de 30 segundos e o subprocesso termina após devolver os dados. Apenas o último retrato permanece em memória. A interface não faz polling da rede: seu timer apenas verifica a fila de resultados.

Evite Electron, Docker e várias máquinas virtuais nesta primeira etapa. Para Linux, adicione posteriormente um laboratório WSL2 e execute um ambiente por vez. Planeje inicialmente até 2 GB para o laboratório, ajustando após medir o Windows e as ferramentas. Esse valor é uma proposta, não uma medição. Nenhum componente Linux é instalado nesta entrega.

## Testes

Na pasta do projeto:

```powershell
python -m unittest discover -s tests -v
python -m blackbird --snapshot
```

O segundo comando imprime dados reais locais: evite publicar sua saída sem revisar os endereços e processos.

Roteiro manual autorizado, no seu computador:

1. Consulte a rede e compare IP/gateway com `ipconfig`; compare PIDs com o Gerenciador de Tarefas.
2. Em um segundo terminal, execute `python -m http.server 8765 --bind 127.0.0.1`. O servidor disponibiliza arquivos da pasta atual apenas no loopback; execute em uma pasta vazia de laboratório.
3. Atualize o inspector e filtre por `8765`: deve aparecer `Listen` em `127.0.0.1`.
4. Abra `http://127.0.0.1:8765` no navegador. Conexões estabelecidas podem durar pouco: não é obrigatório capturá-las em um retrato manual.
5. Encerre o servidor com Ctrl+C e consulte novamente. O listener deve desaparecer.
6. Exporte JSON e confira as listas `interfaces`, `tcp` e o horário UTC `captured_at`. O filtro da tela não reduz a exportação.
7. Durante a coleta, mova a janela: ela deve continuar respondendo, e o botão de consulta deve ficar desabilitado até o término.
8. Meça o processo Python e o PowerShell no Gerenciador de Tarefas, antes/durante/depois da coleta. Repita dez consultas e observe se a memória estabiliza. Não foi definido um consumo garantido para todos os notebooks.

## Próximas entregas e estudos até 2030

Esta é uma trilha proposta a partir do pedido disponível; as respostas completas da conversa anterior não puderam ser recuperadas.

| Etapa | Estudos | Entrega prática |
|---|---|---|
| 2026–2027 | Python, Git, testes, processos, TCP/IP, DNS, sub-redes | Network Inspector; diário de exercícios local em SQLite; leitor de logs |
| 2027 | Linux, permissões, shell, serviços, SSH, firewall | Laboratório WSL2 com exercícios e checklist de administração |
| 2028 | HTTP, autenticação, Java e orientação a objetos, segurança de aplicações | Aplicação Java local com falhas didáticas e respectivas correções; testes em laboratório próprio |
| 2029 | Análise de logs, resposta a incidentes, detecção e hardening | Módulo defensivo com eventos sintéticos e relatórios de investigação |
| 2030 | Avaliação ofensiva autorizada, validação de correções, documentação | Projeto integrado de ataque/detecção/correção em laboratório isolado e relatório de escopo |

Python inicia a ferramenta e a automação. Java entra como segunda linguagem para aprofundar aplicações e seus controles de segurança. O primeiro exercício de programação é adicionar uma visualização UDP usando um coletor separado e testes, sem misturar consultas com widgets.

## Referências técnicas

- Tkinter: https://docs.python.org/3/library/tkinter.html
- Get-NetTCPConnection: https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-nettcpconnection
- NetTCPIP: https://learn.microsoft.com/en-us/powershell/module/nettcpip/
