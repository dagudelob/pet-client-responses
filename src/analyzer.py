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
            "red_avoid": ["Do not sound defensive or diagnose medical conditions."],
            "yellow_monitor": ["Monitor slight mood shifts, appetite, or sensitive stomach."],
            "green_prioritize": ["Send timely updates with a warm tone and high-quality photo proofs."]
        },
        "default_clarification_questions": [
            "Does the pet have any additional symptoms or recent medical history?",
            "Are there specific dietary restrictions or a preferred emergency vet?",
            "Do you prefer photo updates or short text summaries during each visit?"
        ]
    }

def evaluate_incident(message: str) -> Dict[str, Any]:
    """
    Analyzes incoming Rover customer messages/notifications,
    classifies the risk level, and generates the traffic light strategy and response options.
    """
    rules = load_rules()
    msg_lower = (message or "").lower()

    # Detect incident keywords
    is_health_issue = any(k in msg_lower for k in [
        "stomach", "vomit", "sick", "diarrhea", "pain", "limp", "blood", "medication", "pill", "tummy", "vet"
    ])
    is_schedule_issue = any(k in msg_lower for k in [
        "late", "time", "hour", "key", "delay", "cancel", "lockbox", "arrive", "early"
    ])
    is_behavior_issue = any(k in msg_lower for k in [
        "bark", "bite", "aggressive", "scared", "shy", "fear", "anxious", "nervous", "pull"
    ])

    if is_health_issue:
        red_text = "🔴 **Avoid:** Do not attempt veterinary diagnoses, do not downplay symptoms, and avoid unauthorized treats or medication."
        yellow_text = "🟡 **Monitor:** Keep close track of hydration, bathroom routines, energy levels, and any abrupt behavioral changes."
        green_text = "🟢 **Prioritize:** Acknowledge promptly with immediate reassurance, share clear photo updates, and ask for vet emergency info if symptoms persist."
        clarifications = [
            "Has the pet experienced vomiting, diarrhea, or appetite loss prior to the visit?",
            "Are there prescribed emergency medications or specific vet care instructions?",
            "Are there authorized treats or a strict sensitive-diet protocol for today?"
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
        red_text = "🔴 **Avoid:** Do not confront the pet, force interactions with other dogs, or take unnecessary public sidewalk risks."
        yellow_text = "🟡 **Monitor:** Observe body language (ears, tail, posture alerts), distance from stimuli, and sensitivity to loud noises."
        green_text = "🟢 **Prioritize:** Maintain safe distance, apply positive reinforcement, and reassure the pet parent with calm patience."
        clarifications = [
            "What are their primary triggers (large dogs, bikes, loud traffic, strangers)?",
            "What rewards or redirection commands work best when they feel stressed?",
            "Would you prefer a quiet, low-traffic route for today's walk?"
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
        red_text = "🔴 **Avoid:** Overpromising unrealistic arrival times or delaying communication when unexpected bottlenecks occur."
        yellow_text = "🟡 **Monitor:** Transit delays, owner availability, and lockbox/entry access instructions."
        green_text = "🟢 **Prioritize:** Confirm an exact estimated time of arrival (ETA) and maintain transparent, proactive communication."
        clarifications = [
            "Is property access via lockbox, concierge/front desk, or in-person greeting?",
            "Is there a +/- 15 minute flexible window for today's arrival?",
            "Would you like immediate entry and exit check-in notifications?"
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
        red_text = "🔴 **Avoid:** " + rules["guidelines"]["red_avoid"][0]
        yellow_text = "🟡 **Monitor:** " + rules["guidelines"]["yellow_monitor"][0]
        green_text = "🟢 **Prioritize:** " + rules["guidelines"]["green_prioritize"][0]
        clarifications = rules.get("default_clarification_questions", [
            "Are there any specific daily routines or instructions for today's visit?",
            "Are fresh water and walking gear readily accessible near the entrance?",
            "Any additional notes regarding your pet's mood or energy level today?"
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