$(document).ready(() => {
    if (window.location.pathname.match(/competition/)) {

        $.ajax({
            method: "GET",
            url: "http://127.0.0.1:8000/api/v1/competition/" + params["pk"] + "/",
            dataType : 'json',
            headers:{
                "Authorization": cookieStrToObject(document.cookie).Authorization
            },
            success: function(data){
                console.log(data);
                $(".title").text(data.name);
                $(".discription").text(data.description);
                if (data.protocol){
                    $(".title").text(data.name);
                }
            },
            error: function(data){
                console.log('error in check permissions');
                delete_cookie("Authorization");
                // $(location).attr('href',"http://127.0.0.1:8000/loginPage/");
                document.location.reload()

            },
            then: function(){
                console.log(data);
            }
        })
    }

});