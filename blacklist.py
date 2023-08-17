import dns.resolver
import smtplib
import requests
from email.mime.text import MIMEText

# Configuración del servidor de correo y telegram
SMTP_SERVER = 'smtp.dominio.com'
SMTP_PORT = 587
SMTP_USERNAME = 'usuario@dominio.com'
SMTP_PASSWORD = 'contraseña'
SENDER_EMAIL = 'usuario@dominio.com'
RECIPIENT_EMAIL = 'usuario@dominio.com'
TELEGRAM_BOT_TOKEN = 'telegram token'
TELEGRAM_CHAT_ID = 'telegran chat id'

# Dirección IP de tu servidor de correo
SERVER_IP = '1.2.3.4'

# Listas negras a verificar
BLACKLISTS = [
    'zen.spamhaus.org',
    'bl.spamcop.net',
    'b.barracudacentral.org',
    'spam.dnsbl.sorbs.net',
    'dnsbl.sorbs.net',
    'rbl.abuse.ro',
]

def check_blacklists(ip_address):
    blacklist_results = []
    for blacklist in BLACKLISTS:
        try:
            query = '.'.join(reversed(str(ip_address).split("."))) + f".{blacklist}."
            dns.resolver.resolve(query, 'A', lifetime=30)
            blacklist_results.append(f"{blacklist}: BLACKLISTED")
        except dns.resolver.NXDOMAIN:
            blacklist_results.append(f"{blacklist}: OK")

    return blacklist_results

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, [RECIPIENT_EMAIL], msg.as_string())
            print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }

    try:
        response = requests.post(telegram_url, data=data)
        if response.status_code == 200:
            print("Notificación de Telegram enviada exitosamente.")
        else:
            print(f"Error al enviar la notificación de Telegram. Código de estado: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar la notificación de Telegram: {e}")

def main():
    try:
        blacklist_results = check_blacklists(SERVER_IP)
        if any("BLACKLISTED" in result for result in blacklist_results):
            subject = "¡Tu servidor de correo está en una lista negra!"
            body = "\n".join(blacklist_results)
            send_email(subject, body)
            send_telegram_message(f"¡ATENCIÓN! Tu servidor de correo está en una lista negra:\n\n{body}")
        else:
            print("El servidor NO está en ninguna lista negra.")
    except Exception as e:
        print(f"Error durante el chequeo: {e}")

if __name__ == "__main__":
    main()