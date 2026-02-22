"""
Módulo para enviar mensajes a través de WhatsApp
Nota: Para usar Twilio necesitas registrarte en twilio.com
Por ahora, usamos una versión simulada que muestra los mensajes
"""

# IMPORTANTE: Para usar Twilio de verdad, necesitas:
# 1. Crear una cuenta en https://www.twilio.com
# 2. Obtener: ACCOUNT_SID y AUTH_TOKEN
# 3. Configurar en .env

def enviar_whatsapp_simulado(numero: str, mensaje: str):
    """
    Simula envío de WhatsApp (útil para desarrollo)
    En producción, usar Twilio
    """
    print(f"\n📱 Simulación: Enviando a {numero}")
    print(f"Mensaje: {mensaje}\n")
    return {
        "success": True,
        "message": "Mensaje simulado enviado correctamente",
        "numero": numero,
        "timestamp": "2026-02-19 12:00:00"
    }


def enviar_whatsapp_twilio(numero: str, mensaje: str, account_sid: str = None, auth_token: str = None):
    """
    Envía mensajes reales a través de Twilio
    Requiere: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
    """
    try:
        from twilio.rest import Client
        
        # Si no se pasan credenciales, intentar usar desde variables de entorno
        if not account_sid or not auth_token:
            import os
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        
        if not account_sid or not auth_token:
            return enviar_whatsapp_simulado(numero, mensaje)
        
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            from_=os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886"),
            body=mensaje,
            to=f"whatsapp:{numero}"
        )
        
        return {
            "success": True,
            "message_id": message.sid,
            "numero": numero,
            "status": message.status
        }
    except Exception as e:
        # En caso de error, usar simulado
        return enviar_whatsapp_simulado(numero, mensaje)
