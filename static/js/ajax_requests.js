
// _______________________      ajax request functions       _____________________________

function login_user_request(username, password, scrf_token){
    $.ajax({
        method: "POST",
        url: "http://127.0.0.1:8000/auth/login/",
        dataType : 'json',
        headers:{"X-CSRFToken": scrf_token},
        data: {
            "username": username,
            "password": password,
        },
        success: function(data){
            $(location).attr('href',"http://127.0.0.1:8000/");
        },
        error: function(data){
            console.log('error in user session login request');
        },
    })
}

function get_auth_token_request(username, password){
    $.ajax({
        method: "POST",
        url: "http://127.0.0.1:8000/auth/api-token-auth/",
        dataType : 'json',
        data: {
            "username": username,
            "password": password,
        },
        success: function(data, status){
            // set_cookie('Authorization', "Token " + data['token'], exp_m=2, path="/");
            document.cookie = `Authorization = Token ${data['token']}; path=/;`;
            console.log("auth token wrote in")
        },
        error: function(data){
            console.log('error in user token login request');
        },
    })
}

function sign_up_user_request(username, password, scrf_token){
    $.ajax({
        method: "POST",
        url: "http://127.0.0.1:8000/api/v1/auth/users",
        dataType : 'json',
        data: {
            "username": username,
            "password": password,
            // "email": mail,
        },
        headers:{"X-CSRFToken": scrf_token},
        success: function(){ 
            alert("Пользователь зарегистрирован"); 
            $(location).attr('href',"http://127.0.0.1:8000/auth/loginPage/");
        },
    });
}
