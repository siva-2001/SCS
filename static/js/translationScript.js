$(document).ready(() => {
    if (window.location.pathname.match(/liveStream/)){

        const chatSocket = new WebSocket(
            'ws://'+window.location.host+'/ws/chat/'+JSON.parse(document.getElementById('match-id').textContent)+'/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(JSON.parse(e.data).message);
            console.log(data)

            if(data["message_type"] == "action_info"){
                if(data["data"]["signal"] == "START_ROUND"){

                    var startDate = new Date();
                    var time = setInterval(function(){
                        var date = new Date()

                        var seconds = parseInt(((date - startDate) / 1000) % 60);
                        var minutes = parseInt((date - startDate) / 60000);
                        if (seconds < 10) seconds = "0" + seconds;
                        if (minutes < 10) minutes = "0" + minutes;
                        $("#time").text("Время " + minutes + ":" + seconds);
                    }, 1000);
                }

            }


            if(data["message_type"] == "translation_data"){
                if (data["data"]["first_team"]["score"] == 0){
                    clearInterval(time);
                    $("#time").text("00:00");
                }

                $('#first_team_score').text(data["data"]["first_team"]["score"]);
                $('#second_team_score').text(data["data"]["second_team"]["score"]);
                $('#match_score').text(data["data"]["first_team"]["rounds_score"] + " : " + data["data"]["second_team"]["rounds_score"]);
                $("#first_team_name").text(data["data"]["first_team"]["participant_name"]);
                $("#second_team_name").text(data["data"]["second_team"]["participant_name"]);
                var part = data["data"]["first_team"]["rounds_score"] + data["data"]["second_team"]["rounds_score"]
                $("#part").text("Партия №" + part)
            }
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
    }
});