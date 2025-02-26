import requests
import time
import logging

# Configurações
URL_SITE = "http://44.202.246.52/"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1344379819512696954/yOCw1LwbFu8JKfOR7rPgEgWaZkP2A6BspJNgcJHDsDrnb5oecrK6XFQvvr8x6vTvQwZI"
LOG_FILE = "/home/ec2-user/monitoramento.log"

# Configurar logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def verificar_site():
    try:
        resposta = requests.get(URL_SITE, timeout=10)
        if resposta.status_code == 200:
            logging.info(f"Site {URL_SITE} está online.")
            return True
        else:
            logging.warning(f"Site {URL_SITE} retornou código {resposta.status_code}.")
            return False
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar {URL_SITE}: {e}")
        return False

def enviar_notificacao():
    mensagem = {"content": f"🚨 ALERTA! O site {URL_SITE} está fora do ar!"}
    try:
        requests.post(DISCORD_WEBHOOK, json=mensagem)
        logging.info("Notificação enviada ao Discord.")
    except requests.RequestException as e:
        logging.error(f"Erro ao enviar notificação para o Discord: {e}")

if __name__ == "__main__":
    if not verificar_site():
        enviar_notificacao()
