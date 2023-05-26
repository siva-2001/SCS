$(document).ready(() => {
    if (window.location.pathname.match(/liveStream/)){

        var time;
        setTimerValue = function(value){
            var seconds = parseInt(value % 60);
            var minutes = parseInt(value / 60);
            if (seconds < 10) seconds = "0" + seconds;
            if (minutes < 10) minutes = "0" + minutes;
            $("#time").text("Время " + minutes + ":" + seconds);
        }

        const chatSocket = new WebSocket(
            'ws://'+window.location.host+'/ws/volleyballTranslation/'+JSON.parse(document.getElementById('match-id').textContent)+'/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(JSON.parse(e.data).message);

            if(data["message_type"] == "translation_data"){
                console.log(data)
                clearInterval(time);
                var timerValue = data["time"];
                if(data["round_time_is_run"]){ time = setInterval(function(){ setTimerValue(timerValue += 1) }, 1000); }
                else setTimerValue(timerValue)

                if (data["data"]["first_team"]["fieldSide"] == "LEFT" && data["data"]["second_team"]["fieldSide"] == "RIGHT"){
                    $('#left_team_score').text(data["data"]["first_team"]["score"]);
                    $("#left_team_name").text(data["data"]["first_team"]["participant_name"]);
                    $('#right_team_score').text(data["data"]["second_team"]["score"]);
                    $("#right_team_name").text(data["data"]["second_team"]["participant_name"]);
                    $('#match_score').text(data["data"]["first_team"]["rounds_score"] + " : " + data["data"]["second_team"]["rounds_score"]);
                } else {
                    $('#left_team_score').text(data["data"]["second_team"]["score"]);
                    $("#left_team_name").text(data["data"]["second_team"]["participant_name"]);
                    $('#right_team_score').text(data["data"]["first_team"]["score"]);
                    $("#right_team_name").text(data["data"]["first_team"]["participant_name"]);
                    $('#match_score').text(data["data"]["second_team"]["rounds_score"] + " : " + data["data"]["first_team"]["rounds_score"]);
                }

                if (data["part"] == 0) $("#part").text("Партия № 1" + data["part"])
                else $("#part").text("Партия №" + data["part"])
            }
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
            $('#translation_error').text("Связь с сервером потеряна");
            $('#translation-table').hide();
        };
    }
});
