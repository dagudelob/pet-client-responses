"""
mail_listener.py
Módulo base para ingesta y parseo de notificaciones y correos de Rover.
Puede ejecutarse como script independiente o integrarse con el servidor MCP de Gmail.
"""

import os
import re
from typing import Dict, Optional
from pydantic import BaseModel

class RoverMessage(BaseModel):
    client_name: str
    pet_name: str
    subject: str
    body_snippet: str
    received_at: Optional[str] = None

def parse_rover_notification(raw_email_text: str) -> RoverMessage:
    """
    Parsea el contenido de una notificación o mensaje de Rover para extraer
    el nombre del dueño, el nombre de la mascota y el mensaje principal.
    """
    # Expresiones regulares comunes para emails de Rover
    owner_match = re.search(r"(?:from|message from|de)\s+([A-Z][a-zA-Z]+)", raw_email_text, re.IGNORECASE)
    pet_match = re.search(r"(?:for|regarding|about|sobre)\s+([A-Z][a-zA-Z]+)", raw_email_text, re.IGNORECASE)
    
    client_name = owner_match.group(1) if owner_match else "Client"
    pet_name = pet_match.group(1) if pet_match else "Pet"
    
    return RoverMessage(
        client_name=client_name,
        pet_name=pet_name,
        subject="Rover New Message Notification",
        body_snippet=raw_email_text.strip()
    )

if __name__ == "__main__":
    sample_text = "New message from Sarah regarding Charlie: Hi! Charlie has a sensitive stomach today, please keep an eye on him."
    parsed = parse_rover_notification(sample_text)
    print(" Rover Notification Parsed successfully:")
    print(parsed.model_dump_json(indent=2))
