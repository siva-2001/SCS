$(document).ready(() => {
    if (window.location.pathname.match(/liveStream/)){

        var time;
        var pauseTime;

        setTimerValue = function(value){
            var seconds = parseInt(value % 60);
            var minutes = parseInt(value / 60);
            if (seconds < 10) seconds = "0" + seconds;
            if (minutes < 10) minutes = "0" + minutes;
            $("#time").text("Время " + minutes + ":" + seconds);
        }

        setPauseTimerValue = function(value, teamName){
            if( value <= 0) value = 0;
            var seconds = parseInt(value % 60);
            var minutes = parseInt(value / 60);
            if (seconds < 10) seconds = "0" + seconds;
            if (minutes < 10) minutes = "0" + minutes;
            $("#time").text("Перерыв (" + teamName + ") " + minutes + ":" + seconds);
        }

        const chatSocket = new WebSocket(
            'ws://'+window.location.host+'/ws/volleyballTranslation/'+JSON.parse(document.getElementById('match-id').textContent)+'/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(JSON.parse(e.data).message);


            console.log(data)


            if(data['message_type'] == "action_info"){
                if(data["data"]["signal"] == "PAUSE_ROUND"){
                    timerValue = 60;
                    pauseTime = setInterval(function(){ setPauseTimerValue(timerValue -= 1, data["data"]["team"]) }, 1000);

                }
            }

            if(data['message_type'] == "action_info"){
                if(data["data"]["signal"] == "STOP_MATCH"){
                    $('#translation_error').text("Матч завершён");
                    $('#translation-table').hide();
                }
            }


            if(data['message_type'] == "action_info"){
                if(data["data"]["signal"] == "CONTINUE_ROUND"){
                    clearInterval(pauseTime);
                }
            }

            if(data["message_type"] == "translation_data"){
                console.log(data)
                clearInterval(time);
                var timerValue = data["time"];
                if(data["round_time_is_run"]){ time = setInterval(function(){ setTimerValue(timerValue += 1) }, 1000); }
                else setTimerValue(timerValue)

                $('#left_team_serve').hide();
                $('#right_team_serve').hide();

                if (data["data"]["first_team"]["fieldSide"] == "LEFT" && data["data"]["second_team"]["fieldSide"] == "RIGHT"){
                    $('#left_team_score').text(data["data"]["first_team"]["score"]);
                    $("#left_team_name").text("Команда " + data["data"]["first_team"]["participant_name"]);
                    $('#right_team_score').text(data["data"]["second_team"]["score"]);
                    $("#right_team_name").text("Команда " + data["data"]["second_team"]["participant_name"]);
                    $('#match_score').text(data["data"]["first_team"]["rounds_score"] + " : " + data["data"]["second_team"]["rounds_score"]);
                    if(data["servesTheBall"] == data["data"]["first_team"]["participant_name"])
                       $('#left_team_serve').show();
                    else $('#right_team_serve').show();

                } else {
                    $('#left_team_score').text(data["data"]["second_team"]["score"]);
                    $("#left_team_name").text("Команда " + data["data"]["second_team"]["participant_name"]);
                    $('#right_team_score').text(data["data"]["first_team"]["score"]);
                    $("#right_team_name").text("Команда " + data["data"]["first_team"]["participant_name"]);
                    $('#match_score').text(data["data"]["second_team"]["rounds_score"] + " : " + data["data"]["first_team"]["rounds_score"]);
                    if(data["servesTheBall"] == data["data"]["first_team"]["participant_name"])
                       $('#right_team_serve').show();
                    else $('#left_team_serve').show();

                }
                $("#part").text("Партия №" + data["part"])
            }

            if (data["ERROR"]){
                $('#translation_error').text(data["ERROR"]);
                $('#translation-table').hide();
            }
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
            $('#translation_error').text("Связь с сервером потеряна");
            $('#translation-table').hide();
        };
    }
});
