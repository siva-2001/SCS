$(document).ready(() => {
    if (window.location.pathname.match(/competition/)) {

        $.ajax({
            method: "GET",
            url: "http://127.0.0.1:8000/api/v1/competition/" + getPK() + "/",
            dataType : 'json',
            headers:{
                "Authorization": cookieStrToObject(document.cookie).Authorization
            },
            success: function(data){
                console.log(data);
                $(".title").text(data.name);

//                <a  data-bs-toggle="collapse" href="#collapseCompetitionEdit" role="button" aria-expanded="false" aria-controls="collapseExample">
//                    <img src="{% static 'pancil_black.png' %}" width="25" height="25">
//                </a>

                $(".description").text(data.description);
                if (data.status == "ANNONCED") $("#organizer").append("Соревнования начнутся: <br>" + data.dateTimeStartCompetition.split(" ")[1]);
                else if (data.status == "PAST") $("#organizer").text("Соревнования завершились: " + data.dateTimeStartCompetition.split(" ")[1]);
//                else if (data.status == "CURRENT") $("#organizer").append("Соревнования начнутся: <br>" + data.dateTimeStartCompetition);
//              Время следующего матча извлекается из запроса к другому урлу

                if (data.protocol) $(".protocol").append(
                    "<a href='" + data.protocol.url + "' download>"
                        + '<p class="h3">Скачать протокол</p>'
                    + '</a>'
                );
                if (data.regulations) $(".regulations").append(
                    "<a href='" + data.protocol.url + "' download>"
                        + '<p class="h3">Скачать регламент</p>'
                    + '</a>'
                );
            },
            error: function(data){
                console.log('error in load competition data');
            },
            then: function(){
                console.log(data);
            }
        })
    }

});