import json
import os
from typing import Dict, Any, List

RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "rules.json")

def load_rules() -> Dict[str, Any]:
    if os.path.exists(RULES_PATH):
        try:
            with open(RULES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "guidelines": {
            "red_avoid": ["Evitar respuestas a la defensiva o diagnósticos médicos."],
            "yellow_monitor": ["Monitorear cambios leves de humor, apetito o digestión."],
            "green_prioritize": ["Notificar a tiempo con tono cálido y fotos de soporte."]
        },
        "default_clarification_questions": [
            "¿Presenta algún síntoma adicional o antecedente médico reciente?",
            "¿Hay indicaciones de dieta especial o veterinario de preferencia?",
            "¿Prefiere actualizaciones por foto o texto breve en cada paseo?"
        ]
    }

def evaluate_incident(message: str) -> Dict[str, Any]:
    """
    Analiza el mensaje entrante del dueño de mascota o notificación de Rover,
    clasificando el nivel de riesgo y generando estrategia de semáforo y respuestas.
    """
    rules = load_rules()
    msg_lower = (message or "").lower()

    # Detectar palabras clave de alerta
    is_health_issue = any(k in msg_lower for k in ["stomach", "vomit", "sick", "diarrhea", "pain", "limp", "blood", "medication", "pill", "estómago", "vómito", "enfermo"])
    is_schedule_issue = any(k in msg_lower for k in ["late", "time", "hour", "key", "delay", "cancel", "tarde", "hora", "cancelar", "llave"])
    is_behavior_issue = any(k in msg_lower for k in ["bark", "bite", "aggressive", "scared", "shy", "fear", "ladra", "muerde", "miedo"])

    if is_health_issue:
        red_text = "🔴 **Evitar:** No des diagnósticos veterinarios, no minimices el síntoma ni des alimentos o premios fuera de su dieta autorizada."
        yellow_text = "🟡 **Monitorear:** Vigilar hidratación, deposiciones, niveles de energía y cualquier cambio conductual súbito."
        green_text = "🟢 **Priorizar:** Confirmar recepción del aviso, tranquilidad inmediata, reportar con fotos claras y solicitar contacto del veterinario si empeora."
        clarifications = [
            "¿Ha tenido vómitos, diarrea o inapetencia antes del paseo o en horas recientes?",
            "¿Tiene medicamentos prescritos o instrucciones veterinarias de emergencia?",
            "¿Hay premios o alimentos específicos autorizados para hoy?"
        ]
        option_a = (
            "Hi [Owner's Name]! Thank you for letting me know about [Pet's Name]'s sensitive tummy. "
            "I'll keep a very close watch on him during our walk, avoid all treats, and ensure he stays calm and comfortable. "
            "I'll send you an update with photos right after! 🐾"
        )
        option_b = (
            "Hi [Owner's Name]! Thank you so much for the heads-up regarding [Pet's Name]. "
            "His health and safety are my top priority. I'll make sure our walk is gentle, low-stress, and keep him from sniffing or snacking on anything along the route. "
            "I will also skip extra treats today to be safe and ensure he has plenty of fresh water. "
            "I'll send you a detailed update with photos as soon as we finish. Please feel free to share any veterinary notes if needed! 🐾"
        )
    elif is_behavior_issue:
        red_text = "🔴 **Evitar:** No confrontar a la mascota, no forzar interacciones con otros perros ni asumir riesgos en la vía pública."
        yellow_text = "🟡 **Monitorear:** Lenguaje corporal (orejas, cola, postura de alerta), distancia de estímulos y tolerancia a ruidos."
        green_text = "🟢 **Priorizar:** Mantener distancia segura, usar refuerzo positivo y transmitir paciencia y confianza al dueño."
        clarifications = [
            "¿Cuáles son sus detonantes habituales (perros grandes, bicicletas, personas extrañas)?",
            "¿Qué recompensas o comandos de redirección le funcionan mejor en momentos de estrés?",
            "¿Prefiere una ruta tranquila y con baja afluencia para este paseo?"
        ]
        option_a = (
            "Hi [Owner's Name]! Got it. I will keep [Pet's Name] on a short, comfortable leash and stick to quiet areas to keep things calm and stress-free. "
            "Photos and updates coming your way shortly! 🐾"
        )
        option_b = (
            "Hi [Owner's Name]! Thank you for the important context about [Pet's Name]. "
            "I'll tailor our route to keep our distance from potential triggers and focus on positive reinforcement to ensure he feels completely secure and happy with me. "
            "I'll keep you posted with photos and notes on how he responded. Thanks for trusting me with his care! 🐾"
        )
    elif is_schedule_issue:
        red_text = "🔴 **Evitar:** Comprometerse a horarios imposibles o dejar de responder ante imprevistos."
        yellow_text = "🟡 **Monitorear:** Tiempos de desplazamiento, disponibilidad del dueño y entrega o recepción de llaves/códigos."
        green_text = "🟢 **Priorizar:** Confirmar la hora exacta estimada de llegada (ETA) y mantener comunicación proactiva y transparente."
        clarifications = [
            "¿El acceso es por caja de llaves (lockbox), conserjería o entrega presencial?",
            "¿Hay flexibilidad de +/- 15 minutos en el horario de inicio?",
            "¿Requiere confirmación inmediata al entrar y salir del domicilio?"
        ]
        option_a = (
            "Hi [Owner's Name]! Thanks for the update regarding the schedule. "
            "I can absolutely adjust to that timing. I will message you the moment I arrive to care for [Pet's Name]! 🐾"
        )
        option_b = (
            "Hi [Owner's Name]! Thanks for reaching out about the schedule. "
            "Everything is noted and I've updated my route accordingly. I'll make sure [Pet's Name] receives his full care and attention, and I'll send you check-in and check-out updates with photos. "
            "Looking forward to seeing him! 🐾"
        )
    else:
        red_text = "🔴 **Evitar:** " + rules["guidelines"]["red_avoid"][0]
        yellow_text = "🟡 **Monitorear:** " + rules["guidelines"]["yellow_monitor"][0]
        green_text = "🟢 **Priorizar:** " + rules["guidelines"]["green_prioritize"][0]
        clarifications = rules.get("default_clarification_questions", [
            "¿Hay alguna indicación o rutina específica a considerar hoy?",
            "¿Disponibilidad de agua fresca y ubicación de accesorios lista?",
            "¿Algún detalle extra sobre el estado de ánimo o energía de la mascota?"
        ])
        option_a = (
            "Hi [Owner's Name]! Thanks for your message. Everything is all set for [Pet's Name]. "
            "I'll take great care of him and send you photos and a summary right after our visit! 🐾"
        )
        option_b = (
            "Hi [Owner's Name]! Thank you for reaching out. I'm really looking forward to caring for [Pet's Name] today! "
            "I'll make sure he follows his routine, gets plenty of love and playtime, and stays happy and safe. "
            "I will send you a complete Rover Card with pictures and updates right after our session. Have a wonderful day! 🐾"
        )

    return {
        "clarification_questions": clarifications,
        "traffic_light": {
            "red": red_text,
            "yellow": yellow_text,
            "green": green_text
        },
        "response_variants": {
            "option_a": option_a,
            "option_b": option_b
        }
    }