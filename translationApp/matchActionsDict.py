
actionsDict = {
    "volleyball":{
        "general_events":[
            {
                "signal":"START_ROUND",
                "button_string":"Начать раунд",
                "button_color":"67CD6B",
                "description":"Запускает новый игровой раунд. Кнопка не должна сущестововать одновременно с CONTINUE_ROUND и PAUSE_ROUND кнопкой. Должно иметь всплывающее окно подтверждения действия",
            },
            {
                "signal":"CONTINUE_ROUND",
                "button_string":"Продолжить игру",
                "button_color":"67CD6B",
                "description":"Возобнавляет счёт времени игрового раунда. Кнопка не должна сущестововать одновременно с PAUSE_ROUND кнопкой. Должно иметь всплывающее окно подтверждения действия",
            },
            {
                "signal": "SWAP_FIELD_SIDE",
                "button_string": "Сменить стороны",
                "description": "Меняет местами стороны поля.  Должно иметь всплывающее окно подтверждения действия",
                "button_color" : "6B67CD"
            },
            {
                "signal":"STOP_MATCH",
                "button_string":"Завершить матч",
                "button_color":"_C50404",
                "description":"Преждевременно завершает матч. Кнопка не должна сущестововать одновременно с START_ROUND кнопкой. Должно иметь всплывающее окно подтверждения действия",
            },
        ],
        "team_events":[
            {
                "signal":"GOAL",
                "button_string":"Гол",
                "button_color":"67CD6B",
                "description":"Засчитывает гол указанной команде"
            },
            {
                "signal": "PAUSE_ROUND",
                "button_string": "Перерыв",
                "button_color": "_E26D00",
                "description": "Останавливает счёт времени игрового раунда. Кнопка не должна быть активна одновременно с CONTINUE_ROUND кнопкой. Не должна быть активной когда translationDataMessage['data']['TEAMNUMBER_team']['pauseCount'] >= 2.  Должно иметь всплывающее окно подтверждения действия",
            },
            {
                "signal": "CANCEL",
                "button_string": "Отменить последний гол",
                "description": "Отменяет последний гол. Кнопка активна только если последний гол был забит выбранной командой.  Должно иметь всплывающее окно подтверждения действия",
                "button_color": "CD6B67",
            },
        ]
    }
}