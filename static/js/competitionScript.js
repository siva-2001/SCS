$(document).ready(() => {
    if (window.location.pathname.match(/competition/)) {

        $.ajax({
            method: "GET",
            url: "http://127.0.0.1:8000/api/v1/competition/" + getPK() + "/",
            dataType : 'json',
            headers:{
                "Authorization": cookieStrToObject(document.cookie).Authorization
            },
            success: function(competition_data){
//                console.log(competition_data);

                $(".title").append(competition_data.name);
                $(".description").text(competition_data.description);
                if (competition_data.status == "ANNONCED") $("#organizer").append("Соревнования начнутся: <br>" + competition_data.dateTimeStartCompetition.split(" ")[1]);
                else if (competition_data.status == "PAST") $("#organizer").text("Соревнования завершились: " + competition_data.dateTimeStartCompetition.split(" ")[1]);


                $.ajax({
                    method: "GET",
                    url: "http://127.0.0.1:8000/api/v1/matchesOfCompetition/" + getPK() + "/",
                    dataType : 'json',
                    headers:{
                        "Authorization": cookieStrToObject(document.cookie).Authorization
                    },
                    success: function(matches_data){
                        if (competition_data.status == "CURRENT") {
                            var nextMatchDateTime;
                            for (i = 0; i < matches_data.length; i++){
                                match_data = matches_data[i];
                                if(match_data.isAnnounced && !match_data.match_translated_now){
                                    nextMatchDateTime = match_data.matchDateTime;
                                    break;
                                }
                            }
                            if(nextMatchDateTime) $("#organizer").append("Следующий матч пройдёт: <br>" + nextMatchDateTime);
                            else $("#organizer").text("Время следующего матча не определено")

                            console.log(matches_data)



                        }
                    },
                    error: function(data){
                        console.log('error in load competition data');
                    },
                })



                if (competition_data.protocol) $(".protocol").append(
                    "<a href='" + competition_data.protocol+ "' download>"
                        + '<p class="h3">Скачать протокол</p>'
                    + '</a>'
                );
                if (competition_data.regulations) $(".regulations").append(
                    "<a href='" + competition_data.protocol + "' download>"
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


