LEXICON: dict[str, str | list[str]] = {
    # -----------------------------   USER   ----------------------------- #
    "hotel_emojis" : ["🏨", "🏝️", "🏖️", "🌴", "🌊", "🌅", "🌺", "🌞", "🍹", "🛎️"],
    "recommendation" :  "👤 <b>Клиент:</b> <i>{}</i>\n\n"
                        "✨ <b>Рекомендации по отелям:</b>\n{}",
    "no_recommendations" : "👤 <b>Клиент:</b> <i>{}</i>\n❗️ Нет рекомендаций по отелям.",
    "dev": "⚙️ В разработке...",
    "error_occurred": "Что-то пошло не так... 🤕\n"
                      "Пожалуйста, обратитесь к администрации: @kill_nik_8\n"
                      "Приносим свои извинения.",

    "start": "<b>Привет!</b> 👋\n\n"
             'Тебе повезло! Я бот, который поможет тебе подобрать отель! 😎',

    "help": "Пожалуйста, дайте нам знать, если у вас появились:\n"
            "- Организационные вопросы: @dlanovenko\n"
            "- Технические вопросы по боту: @kill_nik_8\n"
            "- Вопросы по рекомендациям: @dlanovenko и @kirilica_zxr\n\n"
            "Мы всегда рады помочь вам!",
}

buttons: dict[str, str] = {
    # ---------------------   USER   --------------------- #
    "begin_work": "✏️ Начать работу с клиентом",
    "YES": "Да",
    "NO": "Нет",
    "search_client" : "🔍 Найти клиента по ФИО",
    "profile": "👤 Профиль",
    "edit_profile": "️✏️ Изменить информацию о профиле",
    "edit_name": "Изменить ФИО",
    "edit_status": "Изменить статус",
    "help": "ℹ️ Помощь",
    "back_button": "🔙 Назад",
    "menu": "Меню",
    "back_to_menu": "В меню",
    "event_registration_pre-registration": "Предрегистрация",
    "event_registration_standard": "📝 Зарегистрироваться",
    "event_registration_premium": "Премиум",
    "event_registration_fast": "⚡️ Фаст-регистрация",
    "confirm_registration": "✅ Всё верно",
    "cancel_registration": "❌ Отмена",
    "registration_status_other": "Другое",
}

callbacks: dict[str, str] = {
    # ---------------------   USER   --------------------- #
    buttons['begin_work'] : 'begin_work_button',
    buttons['YES'] : 'yes_button',
    buttons['NO'] : 'no_button',
    buttons['search_client'] : 'search_client_button',
    buttons["profile"]: "profile_button",
    buttons["help"]: "help_button",
    buttons[
        "event_registration_pre-registration"
    ]: "register_for_the_event_pre-registration_{}",
    buttons["event_registration_standard"]: "register_for_the_event_standard_{}",
    buttons["event_registration_premium"]: "register_for_the_event_premium_{}",
    buttons["event_registration_fast"]: "register_for_the_event_fast_{}",
    buttons["confirm_registration"]: "registration_confirmed",
    buttons["cancel_registration"]: "registration_canceled",
    # ---------------------   USER   --------------------- #
    buttons["edit_profile"]: "edit_profile_button",
    buttons["edit_name"]: "edit_name_button",
    buttons["edit_status"]: "edit_status_button",
    # ---------------------   Back   --------------------- #
    "profile_registration_back_to_name": "profile_registration_back_to_name",
    "profile_registration_back_to_budget": "profile_registration_back_to_budget",
    "profile_registration_back_to_region": "profile_registration_back_to_region",
    "profile_registration_back_to_trip_type" : "profile_registration_back_to_trip-type",
    "profile_registration_back_to_date_of_birth": "profile_registration_back_to_date-of-birth",
    "profile_registration_back_to_status": "profile_registration_back_to_status",
    "profile_registration_back_to_phone_number": "profile_registration_back_to_phone-number",
    "back_to_profile": "back_to_profile_button",
}