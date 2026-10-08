# ============================================================
# SISTEMA DE RECOMPENSAS POR NÍVEL
# ============================================================


LEVEL_REWARDS = {
    1: {
        "name": "Iniciante",
        "reward": "Acesso ao sistema PetroQuiz",
        "icon": "🛢️"
    },

    2: {
        "name": "Aprendiz",
        "reward": "Distintivo de Aprendiz",
        "icon": "📚"
    },

    3: {
        "name": "Técnico",
        "reward": "Distintivo Técnico",
        "icon": "⚙️"
    },

    4: {
        "name": "Explorador",
        "reward": "Distintivo Explorador",
        "icon": "🧭"
    },

    5: {
        "name": "Especialista",
        "reward": "Distintivo Especialista",
        "icon": "🎓"
    },

    6: {
        "name": "Engenheiro",
        "reward": "Distintivo Engenheiro",
        "icon": "👷"
    },

    7: {
        "name": "Mestre do Petróleo",
        "reward": "Distintivo Mestre do Petróleo",
        "icon": "🏆"
    },

    8: {
        "name": "Lenda do Petróleo",
        "reward": "Distintivo Lenda do Petróleo",
        "icon": "👑"
    }
}


def get_level_reward(level):
    """
    Retorna a recompensa correspondente ao nível.
    """

    return LEVEL_REWARDS.get(level)


def get_all_rewards():
    """
    Retorna todas as recompensas disponíveis.
    """

    return LEVEL_REWARDS


def get_reward_name(level):
    """
    Retorna apenas o nome da recompensa.
    """

    reward = get_level_reward(level)

    if reward:
        return reward["reward"]

    return None


def get_reward_icon(level):
    """
    Retorna o ícone da recompensa.
    """

    reward = get_level_reward(level)

    if reward:
        return reward["icon"]

    return "🎁"