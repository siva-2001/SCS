$(document).ready(() => {
    if (window.location.pathname.match(/liveStream/)){

        const chatSocket = new WebSocket(
            'ws://'+window.location.host+'/ws/chat/'+JSON.parse(document.getElementById('match-id').textContent)+'/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(JSON.parse(e.data).message);
            console.log(data)

            if(data["message_type"] == "translation_data"){
                $('#first_team_score').text(data["data"]["first_team"]["score"]);
                $('#second_team_score').text(data["data"]["second_team"]["score"]);
                $('#match_score').text(data["data"]["first_team"]["rounds_score"] + " : " + data["data"]["second_team"]["rounds_score"]);
                $("#first_team_name").text(data["data"]["first_team"]["participant_name"]);
                $("#second_team_name").text(data["data"]["second_team"]["participant_name"]);
            }
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
    }
});