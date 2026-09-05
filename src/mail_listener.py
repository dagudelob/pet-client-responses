"""
mail_listener.py
Módulo para ingesta y parseo de correos de Rover desde Gmail API o entrada directa.
"""

import os
import re
import json
import base64
from typing import Dict, Optional, List
from pydantic import BaseModel

class RoverMessage(BaseModel):
    client_name: str
    pet_name: str
    subject: str
    body_snippet: str
    received_at: Optional[str] = None
    source: str = "direct"  # "direct", "paste", "gmail"

def parse_rover_notification(raw_email_text: str, source: str = "direct") -> RoverMessage:
    """
    Parsea el contenido de una notificación o mensaje de Rover para extraer
    el nombre del dueño, el nombre de la mascota y el mensaje principal.
    Soporta formatos comunes de emails de Rover o mensajes copiados y pegados.
    """
    text = raw_email_text.strip()
    
    # 1. Buscar nombre del dueño
    owner_match = re.search(
        r"(?:from|message from|de|mensaje de|owner|client|dueño):\s*([A-Za-zÀ-ÿ]+)|(?:from|de)\s+([A-Za-zÀ-ÿ]+)\b",
        text,
        re.IGNORECASE
    )
    client_name = "Sarah"
    if owner_match:
        client_name = (owner_match.group(1) or owner_match.group(2)).strip().capitalize()
    else:
        # Intento de capturar al inicio como "Sarah:" o "Sarah -"
        prefix_match = re.match(r"^([A-Za-zÀ-ÿ]{2,15})[:\s-]", text)
        if prefix_match:
            client_name = prefix_match.group(1).capitalize()

    # 2. Buscar nombre de la mascota
    pet_match = re.search(
        r"(?:for|regarding|about|sobre|mascota|pet|dog|perro):\s*([A-Za-zÀ-ÿ]+)|(?:for|regarding|about|sobre)\s+([A-Za-zÀ-ÿ]+)\b",
        text,
        re.IGNORECASE
    )
    pet_name = "Charlie"
    if pet_match:
        pet_name = (pet_match.group(1) or pet_match.group(2)).strip().capitalize()

    # 3. Limpiar el cuerpo del mensaje si viene con cabeceras de email
    clean_body = text
    # Si contiene separadores típicos de emails
    body_match = re.search(r"(?:Subject|Asunto):.*?\n\n(.*)", text, re.DOTALL | re.IGNORECASE)
    if body_match:
        clean_body = body_match.group(1).strip()

    return RoverMessage(
        client_name=client_name,
        pet_name=pet_name,
        subject="Rover New Message",
        body_snippet=clean_body,
        source=source
    )

def fetch_messages_from_gmail(credentials_path: str = "credentials.json", token_path: str = "token.json", max_results: int = 5) -> List[RoverMessage]:
    """
    Se conecta a la API de Gmail usando OAuth2 para recuperar correos recientes de Rover.
    Requiere que credentials.json o token.json estén configurados.
    """
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif os.path.exists(credentials_path):
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            else:
                return []

        service = build('gmail', 'v1', credentials=creds)
        # Buscar correos de Rover
        query = "from:rover.com OR subject:Rover"
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])

        rover_msgs = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            snippet = msg_data.get('snippet', '')
            
            headers = msg_data.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'Rover Message')
            
            # Obtener cuerpo si es posible
            body = snippet
            payload = msg_data.get('payload', {})
            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                        break
            elif 'data' in payload.get('body', {}):
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')

            parsed = parse_rover_notification(f"Subject: {subject}\n\n{body}", source="gmail")
            parsed.subject = subject
            rover_msgs.append(parsed)

        return rover_msgs

    except Exception as e:
        print(f"Error al conectar con Gmail API: {e}")
        return []
