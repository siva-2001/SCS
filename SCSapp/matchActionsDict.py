
actionsDict = {

    # signal не должен превышать 20 символов

    "volleyball":{
        "general_events":[
            {
                "signal":"START_ROUND",
                "button_string":"Начать раунд",
                "button_color":"67CD6B",
                "description":"Запускает новый игровой раунд. Кнопка не должна сущестововать одновременно с CONTINUE_ROUND и PAUSE_ROUND кнопкой. Должно иметь всплывающее окно подтверждения действия",
            },
            {
                "signal":"PAUSE_ROUND",
                "button_string":"Остановить игру",
                "button_color":"_E26D00",
                "description":"Останавливает счёт времени игрового раунда. Кнопка не должна сущестововать одновременно с CONTINUE_ROUND кнопкой.  Должно иметь всплывающее окно подтверждения действия",
            },
            {
                "signal":"CONTINUE_ROUND",
                "button_string":"Продолжить игру",
                "button_color":"67CD6B",
                "description":"Возобнавляет счёт времени игрового раунда. Кнопка не должна сущестововать одновременно с PAUSE_ROUND кнопкой. Должно иметь всплывающее окно подтверждения действия",
            },
            {
                "signal":"STOP_MATCH",
                "button_string":"Завершить матч",
                "button_color":"_C50404",
                "description":"Преждевременно завершает матч. Кнопка не должна сущестововать одновременно с START_ROUND кнопкой. Должно иметь всплывающее окно подтверждения действия",
            },
            {
                "signal":"STOP_ROUND",
                "button_string":"Завершить раунд",
                "button_color":"_C50404",
                "description":"Завершает раунд. Кнопка не должна сущестововать одновременно с START_ROUND кнопкой. Должно иметь всплывающее окно подтверждения действия",
            }   
        ],
        "team_events":[
            {
                "signal":"GOAL",
                "button_string":"Гол",
                "button_color":"67CD6B",
                "description":"Засчитывает гол указанной команде"
            },
            {
                "signal":"CANCEL",
                "button_string":"Отмена",
                "description":"Отменяет последнее событие. Обязательно для любого вида спорта"
            },
            {
                "signal":"BREAK",
                "button_string":"Перерыв",
                "description":"Должно также указываться сколько их осталось"
            }
        ]
    }
}