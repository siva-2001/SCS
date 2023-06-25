$(document).ready(() => {
    if (window.location.pathname.match(/competition/)) {

        $.ajax({
            async: false,
            method: "GET",
            url: "http://127.0.0.1:8000/api/v1/competition/" + getPK() + "/",
            dataType : 'json',
            headers:{   "Authorization": cookieStrToObject(document.cookie).Authorization   },
            success: function(competition_data){
                console.log(competition_data)

                $(".title").append(competition_data.name);
                $("#competition_title_edit").val(competition_data.name)

                $(".description").text(competition_data.description);
                $("#competition_description_edit").val(competition_data.description)

                if (competition_data.status == "ANNONCED"){
                    $("#start_draw").show();
                    if(competition_data.dateTimeStartCompetition) $$("#organizer").append("Соревнования начнутся: <br>" + competition_data.dateTimeStartCompetition.split(" ")[1]);
                    else $("#organizer").text("Время начала соревнований не определено");


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
                    async: false,
                    method: "GET",
                    url: "http://127.0.0.1:8000/api/v1/matchesOfCompetition/" + getPK() + "/",
                    dataType : 'json',
                    headers:{   "Authorization": cookieStrToObject(document.cookie).Authorization   },
                    success: function(matches_data){
                        console.log(matches_data);
                        console.log(competition_data.status);

                        if (competition_data.status == "CURRENT") {
                            var nextMatchDateTime;
                            var competitionStage = "-";

                            if (matches_data.length != 0) $("#tournament_grid_block").show();

                            for (var i = 0; i < matches_data.length; i++){
                                match_data = matches_data[i];

//                                if (competitionStage != match_data["competitionStage"]){
//                                    competitionStage = match_data["competitionStage"];
//                                    addCompetitionStage(competitionStage);
//                                }
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
                        console.log(teams_data);
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

        $('.send_edit_match').on('click', e => {
            var formData = new FormData();

            var id = $(e.target).val();
            console.log($('#match_place_ID_' + id).val());
            console.log($('#match_judge_ID_' + id).val());
            console.log($('#match_datetime_ID_' + id).val());

            if ($('#match_place_ID_' + id).val() === ""
            && $('#match_judge_ID_' + id).val() === ""
            && $('#match_datetime_ID_' + id).val() === ""){
//                alert("Заполните пустые поля");
                return;
            }

            if ($('#match_place_ID_' + id).val() != "") formData.append('place', $('#match_place_ID_' + id).val());
            if ($('#match_judge_ID_' + id).val() != "") formData.append('judge', $('#match_judge_ID_' + id).val());
            if ($('#match_datetime_ID_' + id).val() != "") formData.append('matchDateTime', $('#match_datetime_ID_' + id).val());

            $.ajax({
                    method: "PUT",
                    url: "http://127.0.0.1:8000/api/v1/match/" + id + "/",
                    dataType : 'json',
                    contentType: false,
                    processData: false,
                    cache: false,
                    data: formData,
                    headers:{
                        "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').attr('value'),
                        "Authorization": cookieStrToObject(document.cookie).Authorization
                    },
                }).done(function() {
                    alert('Матч успешно отредактирован!');
                    document.location.reload()
                });
        });

        $("#sendCompetitionEdit").click(() => {
            updateCompetition(
                getPK(),
                $("#competition_title_edit").val(),
                $("#competition_description_edit").val(),
                $("#competition_datetime_edit").val());
        });

        $("#start_draw").click(() => {
            $.ajax({
                async: false,
                method: "POST",
                url: "http://127.0.0.1:8000/api/v1/competition_draw/",
                dataType : 'json',
                contentType: false,
                processData: false,
                cache: false,
                data: '{"competition_id":' + getPK() + '}',
                headers:{
//                        "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').attr('value'),
                    "Authorization": cookieStrToObject(document.cookie).Authorization
                },
            }).always(function(){
                document.location.reload();
            });
        });
    }

    checkAccessPermissions();
});


