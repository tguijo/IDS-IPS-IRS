# Importar el módulo Scapy
from scapy.all import *

# Función para bloquear ataques
def block_attack(pkt):
    # Verificar si el paquete es TCP
    if pkt.haslayer(TCP):
        # Obtener información del paquete
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        src_port = pkt[TCP].sport
        dst_port = pkt[TCP].dport
        flags = pkt[TCP].flags

        # Verificar si el paquete contiene una conexión SYN y ACK
        if (flags & 0x12) == 0x12:
            # Bloquear la conexión utilizando el comando iptables
            os.system("iptables -A INPUT -s {} -j DROP".format(src_ip))
            print("[+] Ataque bloqueado: SYN-ACK Scan desde {}:{} hasta {}:{}".format(src_ip, src_port, dst_ip, dst_port))

# Sniffear los paquetes de la red
sniff(prn=block_attack, filter="tcp", store=0)
