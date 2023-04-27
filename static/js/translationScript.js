$(document).ready(() => {
    if (window.location.pathname.match(/liveStream/)){
        // обращение к 'api/v1/matchManagment/', извлечение названия команды


        const chatSocket = new WebSocket(
            'ws://'+window.location.host+'/ws/chat/'+JSON.parse(document.getElementById('match-id').textContent)+'/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log(data.message)
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
    }
});