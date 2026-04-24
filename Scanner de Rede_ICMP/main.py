# ============================================================
#  Scanner de Rede —  NetDevOps
#  Disciplina: Redes de Comunicação de Dados
# ============================================================

import subprocess
import platform
import datetime
import socket

# Configuração
# Entrada e saida do script

IPS_ALVO = [
    "192.168.0.13",
    "192.168.0.1",
    "192.168.1.1",
    "192.168.1.10",
    "192.168.1.20",
    "192.168.1.100",
    "192.168.1.200",
    "8.8.8.8",    # Google DNS
    "1.1.1.1",    # Cloudflare DNS
]
ARQUIVO_SAIDA = "relatorio_rede.txt"

#Tratamento multi plataforma

def montar_comando(ip):
    """Monta o comando de ping correto para cada SO."""
    sistema = platform.system().lower()
    if sistema == "windows":
        return ["ping", "-n", "1", "-w", "1000", ip]
    else:  # Linux / macOS
        return ["ping", "-c", "1", "-W", "1", ip]


def pingar(ip):
    """Envia 1 pacote ICMP e retorna True (UP) ou False (DOWN)."""
    comando = montar_comando(ip)
    resultado = subprocess.run(
        comando,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return resultado.returncode == 0


def escanear_rede(lista_ips):
    """Escaneia todos os IPs e retorna dicionário com status."""
    resultados = {}
    for ip in lista_ips:
        print(f"  Verificando {ip}...", end=" ")
        status = pingar(ip)
        resultados[ip] = status
        rotulo = "UP  ✓" if status else "DOWN ✗"
        print(rotulo)
    return resultados


def salvar_relatorio(resultados, arquivo):
    """Gera relatório .txt com hosts UP e DOWN."""
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ups   = [ip for ip, ok in resultados.items() if ok]
    downs = [ip for ip, ok in resultados.items() if not ok]

    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(f"RELATÓRIO DE REDE — {agora}\n")
        f.write("=" * 40 + "\n\n")

        f.write(f"HOSTS UP ({len(ups)}):\n")
        for ip in ups:
            f.write(f"  [UP]   {ip}\n")

        f.write(f"\nHOSTS DOWN ({len(downs)}):\n")
        for ip in downs:
            f.write(f"  [DOWN] {ip}\n")

        f.write(f"\nTOTAL VERIFICADOS: {len(resultados)}\n")

    print(f"\nRelatório salvo em: {arquivo}")


# --- Execução principal ---
if __name__ == "__main__":
    print("=== Scanner de Rede Simples ===")
    
    print("Recuperando IP local...")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    IPS_ALVO.append(local_ip)
    print(f"IP local encontrado: {local_ip}")

    print(f"Verificando {len(IPS_ALVO)} hosts...\n")

    resultados = escanear_rede(IPS_ALVO)
    salvar_relatorio(resultados, ARQUIVO_SAIDA)