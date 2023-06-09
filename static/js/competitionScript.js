
function addMatchNote(match_data){

    console.log(match_data);
    datetime = match_data["matchDateTime"] ? match_data["matchDateTime"] : "Время и дата не определены"
    place = match_data['place'] ? match_data['place'] : "Место не определено"
    firstTeamScore = match_data["firstTeamScore"] ? match_data["firstTeamScore"] : ""
    secondTeamScore = match_data["secondTeamScore"] ? match_data["secondTeamScore"] : ""


    html_match_element =
            '<div class="matchNote">'
            + '<div class="row mh-1">'
                + '<div class="col-3">'
                    + '<div class="row mp-3">'
                        + '<p class="p6">' + datetime + '</p>'
                    + '</div>'

    if (match_data["protocol"]){
        html_match_element = html_match_element
            + '<div class="row mt-5 mb-1">'
                + '<a href="http://127.0.0.1:8000/' + match_data["protocol"] + '" download=""> Протокол </a>'
            + '</div>'
    }

    html_match_element = html_match_element
                + '</div>'
                + '<div class="container text-center col">'
                    + '<div class="row score justify-content-md-center mt-2">'
                        + '<div class="col-3"> '
                        + match_data["firstTeam"]

    if (match_data["firstTeamEmblem"])
        html_match_element = html_match_element + ' <img width="50" height="50" src="http://127.0.0.1:8000' + match_data["firstTeamEmblem"] + '"> '


    if(match_data["isAnnounced"])  html_match_element = html_match_element + '</div><div class="col-3">';
    else {
        html_match_element = html_match_element + '</div><div class="col-2">'
        if (firstTeamScore > secondTeamScore)
            html_match_element = html_match_element
                + '<p6 class="p6 winner"> '+ firstTeamScore + ' </p6> : <p6 class="p6 loser"> ' + secondTeamScore + ' </p6>';
        else  html_match_element = html_match_element
            + '<p6 class="p6 loser"> '+ firstTeamScore + ' </p6> : <p6 class="p6 winner"> ' + secondTeamScore + ' </p6>';
        html_match_element = html_match_element + '</div><div class="col-3">';
    }




    if (match_data["secondTeamEmblem"])
        html_match_element = html_match_element + ' <img width="50" height="50" src="http://127.0.0.1:8000' + match_data["secondTeamEmblem"] + '"> '

    html_match_element = html_match_element
                        + match_data["secondTeam"] + '</div>'
                    + '</div>'
                    + '<div class="row justify-content-md-center mt-4">'
                        + '<div class="col"> ' + match_data["roundsScore"] + ' </div>'
                    + '</div>'
                + '</div>'
                + '<div class="col-2">'
                    + '<div class="row mp-3">'
                        + '<p class="p6" align="right">' + place + '</p>'
                    + '</div>'
                + '</div>'
            + '</div>'
        + '</div>'

    $("#tournament_grid").append(html_match_element);
}

function addTeamNote(team_data){
    icon_url = team_data["icon_url"]

    html_team_element =
        '<div class="team">'
            + '<div class="row">'
                + '<div class="col-4 text-center">'
                    + '<img width="50" height="50" src="http://127.0.0.1:8000/' + icon_url + '">'
                    + team_data["name"]
                + '</div>'
                + '<div id="completed" class="col-2 text-center">'
                + team_data["completed"]
                + '</div>'
                + '<div id="won" class="col-2 text-center">'
                    + team_data["won"]
                + '</div>'
                + '<div id="lost" class="col-2 text-center">'
                    + team_data["lost"]
                + '</div>'
                + '<div id="score" class="col-2 text-center">'
                    + team_data["score"]
                + '</div>'
            + '</div>'
        + '</div>'

    $("#teamsList").append(html_team_element);
}

function addCompetitionStage(stage){
    var stageString;
    if(stage == "1/1") stageString = "Финал";
    else if(stage == "1/2") stageString = "Полуфинал";
    else if(stage == "1/4") stageString = "1/4-финал";
    else if(stage == "1/8") stageString = "1/8-финал";
    $("#tournament_grid").append('<div class="competitionStage">' + stageString + '</div>');
}



$(document).ready(() => {
    if (window.location.pathname.match(/competition/)) {

        $("#sendCompetitionEdit").click(() => {
            updateCompetition(
                getPK(),
                $("#competition_title_edit").val(),
                $("#competition_description_edit").val(),
                $("#competition_datetime_edit").val());
        });

        comp_ajax = $.ajax({
            method: "GET",
            url: "http://127.0.0.1:8000/api/v1/competition/" + getPK() + "/",
            dataType : 'json',
            headers:{   "Authorization": cookieStrToObject(document.cookie).Authorization   },
            success: function(competition_data){
                $(".title").append(competition_data.name);
                $("#competition_title_edit").val(competition_data.name)

                $(".description").text(competition_data.description);
                $("#competition_description_edit").val(competition_data.description)

                if (competition_data.status == "ANNONCED"){
                    $("#organizer").append("Соревнования начнутся: <br>" + competition_data.dateTimeStartCompetition.split(" ")[1]);
                    $("#competition_datetime_input_string").show();
                    $("#tournament_grid_block").hide();
                }
                else if (competition_data.status == "PAST")
                    $("#organizer").text("Соревнования завершились: " + competition_data.dateTimeStartCompetition.split(" ")[1]);

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


                $.ajax({
                    method: "GET",
                    url: "http://127.0.0.1:8000/api/v1/matchesOfCompetition/" + getPK() + "/",
                    dataType : 'json',
                    headers:{   "Authorization": cookieStrToObject(document.cookie).Authorization   },
                    success: function(matches_data){
                        if (competition_data.status == "CURRENT") {
                            var nextMatchDateTime;
                            var competitionStage = "-";
                            for (i = 0; i < matches_data.length; i++){
                                match_data = matches_data[i];

                                if (competitionStage != match_data["competitionStage"]){
                                    competitionStage = match_data["competitionStage"];
                                    addCompetitionStage(competitionStage);
                                }
                                addMatchNote(match_data);

                                if(match_data.isAnnounced && !match_data.match_translated_now)
                                    nextMatchDateTime = match_data.matchDateTime;
                            }
                            if(nextMatchDateTime) $("#organizer").append("Следующий матч пройдёт: <br>" + nextMatchDateTime);
                            else $("#organizer").text("Время следующего матча не определено")

                        }
                    },
                    error: function(data){  console.log('error in load competition data');  },
                })




            },
            error: function(competition_data){
                alert("Искомого соревнования не существует");
                $(location).attr('href',"http://127.0.0.1:8000/");

            },
            then: function(){   console.log(competition_data);  }
        })

//        console.log(comp_ajax);
    }

});


