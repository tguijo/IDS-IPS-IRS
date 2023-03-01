# Importar el módulo Scapy
from scapy.all import *

# Función para detectar ataques
def detect_attacks(pkt):
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
            print("[+] Ataque detectado: SYN-ACK Scan desde {}:{} hasta {}:{}".format(src_ip, src_port, dst_ip, dst_port))

# Sniffear los paquetes de la red
sniff(prn=detect_attacks, filter="tcp", store=0)
