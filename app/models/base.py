from datetime import datetime
from zoneinfo import ZoneInfo

FUSO_HORARIO = ZoneInfo("America/Sao_Paulo")


def agora():
    """Data e hora atuais no horário de Brasília (o servidor de hospedagem usa UTC)."""
    return datetime.now(FUSO_HORARIO).replace(tzinfo=None)
