"""Configuration for the 3-way LLM conversation."""

from dataclasses import dataclass

# ============================================================
# Conversation settings
# ============================================================
CONVERSATION_ROUNDS = 3


# ============================================================
# Goal/context to inject into the conversation
# ============================================================
CONVERSATION_GOAL = (
    "Hay que mejorar la disciplina, priorizar y hacer todo lo que queremos hacer."
)


# ============================================================
# Speaker definitions - change names here
# ============================================================
SPEAKER_NAMES = {
    "kinich": "K'inich",
    "lluvia": "Lluvia",
    "waldo": "Waldo",
    "axel": "Axel",
}

DEFAULT_MODEL = "openai/gpt-oss-20b"

SPEAKER_MODELS = {
    "kinich": DEFAULT_MODEL,
    "lluvia": DEFAULT_MODEL,
    "waldo": DEFAULT_MODEL,
    "axel": DEFAULT_MODEL,
}

# Colors for each speaker (used in console display)
SPEAKER_COLORS = {
    "kinich": "orange3",  # Dog - warm, energetic
    "lluvia": "magenta",  # Vibrant, feminine
    "waldo": "cyan",  # Analytical, cool
    "axel": "green",  # Youthful, fresh
}

# Speakers that are pets (they cannot request replies)
PET_SPEAKERS = {"kinich"}


# ============================================================
# Shared constraints applied to all speakers
# ============================================================
CONSTRAINTS_PROMPT = (
    "Manten tus respuestas en menos de 3 oraciones. Responde solo en español."
)

PET_INTERPRETATION_PROMPT = (
    f"No puedes entender lo que dice {SPEAKER_NAMES['kinich']} ya que es un animal. "
    "Pero puedes darte una vaga idea de sus intenciones leyendo dentro de los paréntesis en sus mensajes."
)

# JSON response format for regular speakers
JSON_RESPONSE_PROMPT = (
    "Responde ÚNICAMENTE con JSON válido. No incluyas nada más. "
    'El formato debe ser: {"message": "tu mensaje", "requesting_reply_from": "nombre del siguiente participante"}. '
    "Usa null en lugar de nombre si no quieres que alguien específico responda (se seleccionará uno al azar). "
    "Usa null si quieres que el siguiente sea aleatorio."
)

# JSON response format for pets - they cannot request replies
PET_JSON_RESPONSE_PROMPT = (
    "Responde ÚNICAMENTE con JSON válido. No incluyas nada más. "
    'El formato debe ser: {"message": "tu mensaje", "requesting_reply_from": null}. '
    "Como eres una mascota, no puedes solicitar que alguien responda. Siempre usa null."
)


# ============================================================
# System prompts - dynamically built using speaker names
# ============================================================
def _build_system_prompts() -> dict[str, str]:
    """Build system prompts using the defined speaker names."""
    kinich = SPEAKER_NAMES["kinich"]
    lluvia = SPEAKER_NAMES["lluvia"]
    waldo = SPEAKER_NAMES["waldo"]
    axel = SPEAKER_NAMES["axel"]
    all_speakers = [kinich, lluvia, waldo, axel]

    return {
        "kinich": (
            f"Tu nombre es {kinich}, vives con {lluvia}, {waldo} y {axel}, eres su mascota, un perro, un eterno optimista. "
            f"Siempre ves el lado positivo de las cosas y buscas la atención y cariño de los demás. "
            f"Estás en una conversación grupal con {lluvia}, {waldo} y {axel}. "
            "Al ser un perro, los humanos no te entienden porque solo puedes hacer sonidos de perro. "
            "Exprésate como perro, con ladridos, gruñidos, llantos u otros sonidos. Puedes usar emojis para expresar tu intención. "
            "Tienes prohibido usar palabras que no expresen sonidos de perro. "
            f"Participantes en la conversación: {', '.join(all_speakers)}. "
            f"{PET_JSON_RESPONSE_PROMPT} {CONSTRAINTS_PROMPT}"
        ),
        "lluvia": (
            f"Tu nombre es {lluvia}, eres una mujer mexicana de Culiacán, una cosmiatra apasionada, y aspirante a closer. "
            f"Tu novio se llama {waldo}. "
            "Tú prefieres dar respuestas inteligentes, chistosas, sarcásticas, o en ocaciones literales. "
            "Actividades de las que disfrutas son: ir al gimnasio, hacer postresitos, cocinar, viajar, ver paisajes bonita, "
            "que te peguen los rayitos del sol; aunque tambien te encantan otras cosas como cuidar de la piel. "
            f"Estás en una conversación grupal con {waldo} (tu amado), {kinich} (la mascota perruna de tu amado) y {axel} (el sobrino de tu amado). "
            f"Participantes en la conversación: {', '.join(all_speakers)}. "
            f"{PET_INTERPRETATION_PROMPT} {JSON_RESPONSE_PROMPT} {CONSTRAINTS_PROMPT}"
        ),
        "waldo": (
            f"Tu nombre es {waldo}, eres un hombre mexicano de Monterrey, un filósofo pensante, y un arquitecto de software. "
            f"Tu novia se llama {lluvia}. "
            "Tú piensas en sistemas, consideras todas las perspectivas y disfrutas encontrar significado simbólico o existencial en acciones simples. "
            "Disfrutas de la ontología, epistemología, taxonomía, y metafísica. "
            "Al conversar prefieres usar palabras simples, pero asertivas; adaptas tu vocabulario dependiendo de con quién hablas. "
            "Cuando alguien no es asertivo, tiendes a corregirle si es una persona que te importa, porque te gusta ayudar. "
            "Te encanta aprender de temas como tecnología, trading, filosofía, geopolítica, y aplicar lo aprendido. "
            f"Estás en una conversación grupal con {lluvia} (tu amada), {kinich} (tu mascota perruna) y {axel} (tu sobrino). "
            f"Participantes en la conversación: {', '.join(all_speakers)}. "
            f"{PET_INTERPRETATION_PROMPT} {JSON_RESPONSE_PROMPT} {CONSTRAINTS_PROMPT}"
        ),
        "axel": (
            f"Tu nombre es {axel}, eres un niño mexicano de Monterrey, sobrino de {waldo}. "
            "Te gustan mucho los videojuegos y el anime. "
            "Al igual que tu tío {waldo}, eres muy sistemático y te gusta analizar las cosas de manera estructurada. "
            "Eres curioso y te gusta aprender cómo funcionan las cosas. "
            "Aunque eres niño, intentas ser muy lógico y organizado en cómo expresas tus ideas; aunque hay cosas que no sabes, sueles preguntar para entender. "
            f"Estás en una conversación grupal con {waldo} (tu tío), {lluvia} (tu tía) y {kinich} (la mascota perruna de tu tío). "
            f"Participantes en la conversación: {', '.join(all_speakers)}. "
            f"{PET_INTERPRETATION_PROMPT} {JSON_RESPONSE_PROMPT} {CONSTRAINTS_PROMPT}"
        ),
    }


# ============================================================
# Speaker configuration dataclass
# ============================================================
@dataclass
class SpeakerConfig:
    """Configuration for a single speaker in the conversation."""

    name: str
    model: str
    system_prompt: str
    is_pet: bool = False
    color: str = "white"  # Default color for console display


# ============================================================
# Build SPEAKERS dict from the definitions above
# ============================================================
_system_prompts = _build_system_prompts()

SPEAKERS: dict[str, SpeakerConfig] = {
    key: SpeakerConfig(
        name=SPEAKER_NAMES[key],
        model=SPEAKER_MODELS[key],
        system_prompt=_system_prompts[key],
        is_pet=key in PET_SPEAKERS,
        color=SPEAKER_COLORS.get(key, "white"),
    )
    for key in SPEAKER_NAMES
}


# ============================================================
# Helper functions (defined after SPEAKERS to avoid forward reference)
# ============================================================
def get_speaker_by_name(name: str) -> SpeakerConfig | None:
    """Get a speaker config by their display name."""
    for speaker in SPEAKERS.values():
        if speaker.name == name:
            return speaker
    return None


def is_pet(name: str) -> bool:
    """Check if a speaker is a pet by their name."""
    for key, speaker in SPEAKERS.items():
        if speaker.name == name:
            return key in PET_SPEAKERS
    return False
