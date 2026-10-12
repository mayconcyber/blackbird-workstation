"""Coleta local somente leitura. Não recebe comandos ou alvos do usuário."""
import json
import subprocess
from datetime import datetime, timezone

SCRIPT = r"""
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$interfaces = @(Get-NetIPConfiguration | ForEach-Object {
    [pscustomobject]@{
        name = $_.InterfaceAlias
        index = $_.InterfaceIndex
        ipv4 = @($_.IPv4Address | ForEach-Object { $_.IPAddress })
        ipv6 = @($_.IPv6Address | ForEach-Object { $_.IPAddress })
        gateway = @($_.IPv4DefaultGateway | ForEach-Object { $_.NextHop })
        dns = @($_.DNSServer | ForEach-Object { $_.ServerAddresses })
    }
})
$processes = @{}
Get-Process | ForEach-Object { $processes[[int]$_.Id] = $_.ProcessName }
$tcp = @(Get-NetTCPConnection | ForEach-Object {
    [pscustomobject]@{
        local_address = $_.LocalAddress
        local_port = $_.LocalPort
        remote_address = $_.RemoteAddress
        remote_port = $_.RemotePort
        state = [string]$_.State
        pid = $_.OwningProcess
        process = $processes[[int]$_.OwningProcess]
    }
})
[pscustomobject]@{ interfaces = $interfaces; tcp = $tcp } | ConvertTo-Json -Depth 6 -Compress
"""


def decode_snapshot(raw):
    data = json.loads(raw.lstrip('\ufeff'))
    if not isinstance(data, dict):
        raise ValueError('Resposta de rede inválida.')
    for key in ('interfaces', 'tcp'):
        if not isinstance(data.get(key), list):
            raise ValueError(f'Lista ausente ou inválida: {key}')
        if any(not isinstance(row, dict) for row in data[key]):
            raise ValueError(f'Registro inválido: {key}')
    data['captured_at'] = datetime.now(timezone.utc).isoformat()
    return data


def collect_snapshot():
    try:
        result = subprocess.run(
            ['powershell.exe', '-NoLogo', '-NoProfile', '-NonInteractive', '-Command', SCRIPT],
            capture_output=True, encoding='utf-8', errors='replace', timeout=30,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('A coleta excedeu 30 segundos. Tente novamente.') from exc
    except OSError as exc:
        raise RuntimeError('Não foi possível iniciar o Windows PowerShell.') from exc
    if result.returncode:
        raise RuntimeError('Falha na consulta local: ' + result.stderr.strip()[:1500])
    return decode_snapshot(result.stdout)


def filter_tcp(rows, query):
    query = query.casefold().strip()
    return [row for row in rows if query in ' '.join(str(v) for v in row.values()).casefold()]
