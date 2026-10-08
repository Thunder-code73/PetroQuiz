ACHIEVEMENTS = {

    "first_quiz": {
        "name": "Primeiro Passo",
        "description": "Completa o teu primeiro quiz.",
        "icon": "🛢️"
    },

    "perfect_quiz": {
        "name": "Perfeccionista",
        "description": "Consegue 100% num quiz.",
        "icon": "🎯"
    },

    "five_quizzes": {
        "name": "Aquecendo os Motores",
        "description": "Completa 5 quizzes.",
        "icon": "🔥"
    },

    "hundred_questions": {
        "name": "Mente Petrolífera",
        "description": "Responde a 100 perguntas.",
        "icon": "🧠"
    },

    "level_3": {
        "name": "Técnico",
        "description": "Atinge o nível 3.",
        "icon": "⚙️"
    },

    "level_6": {
        "name": "Engenheiro",
        "description": "Atinge o nível 6.",
        "icon": "👷"
    },

    "level_7": {
        "name": "Mestre do Petróleo",
        "description": "Atinge o nível 7.",
        "icon": "🏆"
    },

    "level_8": {
        "name": "Lenda do Petróleo",
        "description": "Atinge o nível máximo.",
        "icon": "👑"
    },

    "hard_quiz": {
        "name": "Sem Medo do Difícil",
        "description": "Completa um quiz na dificuldade Difícil.",
        "icon": "🛠️"
    },

    "category_explorer": {
        "name": "Explorador",
        "description": "Joga quizzes de 5 categorias diferentes.",
        "icon": "🧭"
    },

    # ====================================================
    # STREAK
    # ====================================================

    "streak_3": {
        "name": "Em Chamas",
        "description": "Completa 3 quizzes consecutivos.",
        "icon": "🔥"
    },

    "streak_10": {
        "name": "Imparável",
        "description": "Completa 10 quizzes consecutivos.",
        "icon": "💥"
    },

    "streak_25": {
        "name": "Lenda Incansável",
        "description": "Completa 25 quizzes consecutivos.",
        "icon": "👑"
    }
}


def get_all_achievements():

    return ACHIEVEMENTS


def get_achievement(achievement_id):

    return ACHIEVEMENTS.get(
        achievement_id
    )


def check_achievements(progress):

    unlocked = progress.get(
        "achievements",
        []
    )

    new_achievements = []

    # ====================================================
    # DADOS PRINCIPAIS
    # ====================================================

    total_quizzes = progress.get(
        "total_quizzes",
        0
    )

    total_questions = progress.get(
        "total_questions",
        0
    )

    level = progress.get(
        "level",
        1
    )

    current_streak = progress.get(
        "current_streak",
        0
    )

    difficulty_played = progress.get(
        "difficulty_played",
        {}
    )

    categories_played = progress.get(
        "categories_played",
        {}
    )

    last_quiz = progress.get(
        "last_quiz",
        {}
    )

    # ====================================================
    # PRIMEIRO QUIZ
    # ====================================================

    if (
        total_quizzes >= 1
        and "first_quiz" not in unlocked
    ):

        new_achievements.append(
            "first_quiz"
        )

    # ====================================================
    # PERFECCIONISTA
    # ====================================================

    if (
        last_quiz.get(
            "percentage",
            0
        ) >= 100

        and "perfect_quiz" not in unlocked
    ):

        new_achievements.append(
            "perfect_quiz"
        )

    # ====================================================
    # 5 QUIZZES
    # ====================================================

    if (
        total_quizzes >= 5
        and "five_quizzes" not in unlocked
    ):

        new_achievements.append(
            "five_quizzes"
        )

    # ====================================================
    # 100 PERGUNTAS
    # ====================================================

    if (
        total_questions >= 100
        and "hundred_questions" not in unlocked
    ):

        new_achievements.append(
            "hundred_questions"
        )

    # ====================================================
    # NÍVEL 3
    # ====================================================

    if (
        level >= 3
        and "level_3" not in unlocked
    ):

        new_achievements.append(
            "level_3"
        )

    # ====================================================
    # NÍVEL 6
    # ====================================================

    if (
        level >= 6
        and "level_6" not in unlocked
    ):

        new_achievements.append(
            "level_6"
        )

    # ====================================================
    # NÍVEL 7
    # ====================================================

    if (
        level >= 7
        and "level_7" not in unlocked
    ):

        new_achievements.append(
            "level_7"
        )

    # ====================================================
    # NÍVEL 8
    # ====================================================

    if (
        level >= 8
        and "level_8" not in unlocked
    ):

        new_achievements.append(
            "level_8"
        )

    # ====================================================
    # QUIZ DIFÍCIL
    # ====================================================

    if (
        difficulty_played.get(
            "Difícil",
            0
        ) >= 1

        and "hard_quiz" not in unlocked
    ):

        new_achievements.append(
            "hard_quiz"
        )

    # ====================================================
    # EXPLORADOR
    # ====================================================

    if (
        len(categories_played) >= 5

        and "category_explorer" not in unlocked
    ):

        new_achievements.append(
            "category_explorer"
        )

    # ====================================================
    # STREAK 3
    # ====================================================

    if (
        current_streak >= 3

        and "streak_3" not in unlocked
    ):

        new_achievements.append(
            "streak_3"
        )

    # ====================================================
    # STREAK 10
    # ====================================================

    if (
        current_streak >= 10

        and "streak_10" not in unlocked
    ):

        new_achievements.append(
            "streak_10"
        )

    # ====================================================
    # STREAK 25
    # ====================================================

    if (
        current_streak >= 25

        and "streak_25" not in unlocked
    ):

        new_achievements.append(
            "streak_25"
        )

    # ====================================================
    # SALVAR NOVAS CONQUISTAS
    # ====================================================

    for achievement_id in new_achievements:

        unlocked.append(
            achievement_id
        )

    progress["achievements"] = unlocked

    return new_achievements