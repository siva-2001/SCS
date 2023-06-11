
function addMatchNote(match_data){
    console.log(match_data);

    var datetime = match_data["matchDateTime"] ? match_data["matchDateTime"] : "Время и дата не определены"
    var place = match_data['place'] ? match_data['place'] : " "
    var firstTeamScore = match_data["firstTeamScore"] ? match_data["firstTeamScore"] : ""
    var secondTeamScore = match_data["secondTeamScore"] ? match_data["secondTeamScore"] : ""

    $.ajax({
        async: false,
        method: "GET",
        url: "http://127.0.0.1:8000/api/v1/judges/",
        dataType : 'json',
        headers:{   "Authorization": cookieStrToObject(document.cookie).Authorization },
        success: function(judges_data){

            var judgeDropdownList = '<select id="match_judge_ID_' + match_data["id"] + '" class="form-select" size="3" aria-label="size 3 select example">'
            for (var j = 0; j < judges_data.length; j++){
                judge_data = judges_data[j];
                str = '<option value=' +judge_data["id"];
                if (match_data["judge"] == judge_data["id"]) str += "   selected";
                str += '>' + judge_data['first_name'] + ' ' + judge_data['last_name'] + '</option>';
                judgeDropdownList += str;
            }
            judgeDropdownList = judgeDropdownList +'</select>';

        html_match_element =
            '<div id="match_ID_' + match_data["id"] + '" class="matchNote">'
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
                        + '<div class="col-3">'
                            + '<div class="row mp-3">'
                                + '<p class="p6" align="right">' + ((place == ' ') ? 'Место не определено' : place) + '</p>'
                            + '</div>'

                            + '<div class="row mt-4">'
                                + '<a id="match_edit_form_ID_' + match_data["id"] + '" data-bs-toggle="collapse" href="#matchEdit_ID_' + match_data["id"] + '" role="button" aria-expanded="false" aria-controls="collapseExample">'
                                    + '<p align="right" class="p6">Редактировать</p>'
                                + '</a>'
                            + '</div>'
                        + '</div>'
                    + '</div>'
                    + '<div  id="matchEdit_ID_' + match_data["id"] + '" class="collapse">'
                        + '<div class="editMatch">'
                            +'<div class="row question">'
                                +'<div class="col-5">'
                                    +'<strong>Где проводится матч?</strong>'
                                +'</div>'
                                +'<div class="col-7">'
                                    +'<input id="match_place_ID_' + match_data["id"] + '" type="text" class="form-control" value="' + place + '">'
                                +'</div>'
                            +'</div>'
                            +'<div class="row question">'
                                +'<div class="col-5">'
                                    +'<strong>Кто судействует?</strong>'
                                +'</div>'
                                +'<div class="col-5">'
                                + judgeDropdownList
                                +'</div>'
                            +'</div>'
                            +'<div class="row question">'
                                +'<div class="col-5">'
                                    +'<strong>Когда пройдёт матч?</strong>'
                                +'</div>'
                                +'<div class="col-3">'
                                    +'<input id="match_datetime_ID_' + match_data["id"] + '" type="datetime-local" class="form-control">'
                                +'</div>'
                                +'<div class="col-4 d-flex align-items-end flex-column">'
                                    +'<button type="submit" id="send_edit_match_btn_ID_' + match_data["id"] + '" class="btn btn-primary pt-3 pb-3 mt-auto">Подвтердить</button>'
                                +'</div>'
                            +'</div>'
                        +'</div>'
                    +'</div>'
                + '</div>'
            $("#tournament_grid").append(html_match_element);
        },
        error: function(data){ console.log('error in load judges data'); },
    });
}

function addTeamNote(team_data){
    icon_url = team_data["icon_url"]

    html_team_element =
        '<div class="team">'
            + '<div class="row">'
                + '<div class="col-4 text-center">'
                    + '<img width="50" height="50" src="http://127.0.0.1:8000' + icon_url + '"> '
                    + team_data["participant_name"]
                + '</div>'
                + '<div id="completed" class="col-2 text-center">'
                + team_data["completed_games"]
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

    $("#teams_list").append(html_team_element);
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


        $("#match_edit_btn").click(() => {
            addEditMatchForm(2);
        });

        $("#sendCompetitionEdit").click(() => {
            updateCompetition(
                getPK(),
                $("#competition_title_edit").val(),
                $("#competition_description_edit").val(),
                $("#competition_datetime_edit").val());
        });

        $.ajax({
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

                            if (matches_data.length != 0) $("#tournament_grid_block").show();


                            for (var i = 0; i < matches_data.length; i++){
                                match_data = matches_data[i];

                                if (competitionStage != match_data["competitionStage"]){
                                    console.log(competitionStage + ' ' + match_data["competitionStage"]);
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

                $.ajax({
                    method: "GET",
                    url: "http://127.0.0.1:8000/api/v1/teamsOfCompetition/" + getPK() + "/",
                    dataType : 'json',
                    headers:{   "Authorization": cookieStrToObject(document.cookie).Authorization },
                    success: function(teams_data){
                        if (teams_data.length > 0) {
                            var number_of_teams = 0;
                            for (var i = 0; i < teams_data.length; i++){
                                if (teams_data[i]["confirmed"]){
                                    addTeamNote(teams_data[i]);
                                    number_of_teams += 1;
                                    $("#teams_list_block").show();
                                }
                            }
                            $("#number_of_teams").append("(" + number_of_teams + ")");
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


