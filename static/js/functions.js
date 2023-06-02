function addAnonymousUserButtons(){
    $(".footer-actions").append(
        "<a href=\"http://127.0.0.1:8000/auth/loginPage/\" id=\"login-head-button\" class=\"menu-btn menu-log-in-btn p-3 me-3 d-block text-center text-decoration-none\">"
        + "Войти"
    + "</a>"
    + "<a href=\"http://127.0.0.1:8000/auth/signupPage/\" id=\"signup-head-button\" class=\"menu-btn menu-log-in-btn p-3 d-block text-center text-decoration-none\">"
        + "Регистрация"
    + "</a>"
    )
}

//        window.location.pathname.split("/").forEach(function(item, i, arr) {
//            if (arr[i-1] == "competition") competition_id = item;
//        });

function getPK(){
    var pk = 0;
    console.log(window.location.pathname);
    window.location.pathname.split("/").forEach(function(item, i, arr) {
        if (!isNaN(parseInt(item))) pk = item;
    });
    return pk;
}

var params = window.location.search.replace('?','').split('&').reduce(
        function(p,e){
            var a = e.split('=');
            p[ decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
            return p;
        },
        {}
    );

function checkAccessPermissions(){
    $.ajax({
        method: "GET",
        url: "http://127.0.0.1:8000/auth/permission/",
        dataType : 'json',
        headers:{
            "Authorization": cookieStrToObject(document.cookie).Authorization 
        },
        success: function(data){
            console.log(data);
            if (data.isAnonymousUser || data.details == "Invalid token.") addAnonymousUserButtons();
            else {
                if(data.isOrganizer) {
                    addCreateEventButton();
                    if(window.location.pathname.match(/competition/)) $("#competitionEditButton").show();
                }
                addProfileElement();
            }
        },
        error: function(data){
            console.log('error in check permissions');
            delete_cookie("Authorization");
            // $(location).attr('href',"http://127.0.0.1:8000/loginPage/");
            document.location.reload()
        
        },
        then: function(){
            document.location.reload()
        }
    })        
}

function addCreateEventButton(){
    $(".footer-actions").append(
        "<button type=\"button\" class=\"menu-btn menu-new-event-btn p-3 d-block text-center text-decoration-none fs-5\">"
            + "Новое соревнование"
        + "</button>"
    )
    $('.menu-new-event-btn').click(() => {
        $(location).attr('href',"http://127.0.0.1:8000/createCompetition/");
    });
    
        // ДЛЯ СПАРТАКИАД
    // $(".footer-actions").append(
    //   "<button type=\"button\" class=\"menu-btn menu-new-event-btn p-3 d-block text-center text-decoration-none fs-5\">"
    //         + "Новое событие"
    //   + "</button>"
    // )
    // $('.menu-new-event-btn').click(() => {
    //     $('.popup-container').css("display", "flex");
    // });
}

function addProfileElement(){
    $(".footer-actions").append(
        "<div class=\"user-profile-item ms-2\">"
          + "<div class=\"item-icons d-flex align-items-center px-2\">"
              +"<svg class=\"me-3 role-icon\" width=\"49\" height=\"35\" viewBox=\"0 0 49 35\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">"
                    +"<path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M4.36792 16.5184L4.79631 15.0433L5.88128 15.1201L6.60193 14.4371L9.14821 17.2297C8.94251 17.6445 8.82032 18.0962 8.7887 18.5589C8.7571 19.0216 8.81669 19.4861 8.96405 19.9254L11.7666 20.1234L14.2768 22.8797L16.4828 20.859L8.27943 12.8771L9.05213 12.1618L8.98807 11.1191L10.4894 10.8483L11.4583 9.95108L7.97516 6.11575L7.02631 6.92404L6.5699 8.40321L5.40485 8.32238L2.32209 10.9776L2.39015 12.1173L0.596531 12.4689L0 12.9781L3.74336 17.0842L4.36792 16.5184ZM26.2235 21.1621L24.8223 34.5918L49 34.8383L47.5307 18.1148C45.8372 16.5589 43.2548 15.5242 40.3803 14.9908L40.1961 16.7367L37.5537 16.6639L40.2281 26.0401L31.5243 25.349L34.1987 16.5791L31.5003 16.5104L31.2521 14.6998L30.3993 14.7321C30.3993 14.7321 15.1256 14.9261 12.8716 14.9261C12.6774 14.9271 12.4835 14.9406 12.291 14.9665L19.2773 20.669L26.2235 21.1621ZM30.6515 12.2103H32.0568C33.8944 14.9019 37.7699 14.7362 39.8998 12.2709H41.5453C44.8403 12.2951 45.3127 8.32642 42.7704 7.19077C43.8834 5.74393 43.2428 3.23015 40.7686 2.8745C38.979 -0.698142 33.5902 -1.19524 31.7365 2.83409C29.1101 2.9715 28.3655 5.6631 29.5305 7.16248C27.1083 8.2658 27.4647 12.186 30.6515 12.2103ZM1.3412 31.6941L0.192169 35L13.2039 34.8181L11.8667 31.6496L1.3412 31.6941Z\" fill=\"#000814\"/>"
              + "</svg>"
              + "<div class=\"icon-container\">"
                +"<svg class=\"arrow\" width=\"19\" height=\"9\" viewBox=\"0 0 19 9\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">"
                        +"<path d=\"M18 1L9.5 7L1 1\" stroke=\"#000814\" stroke-width=\"2\"/>"
                    +"</svg>"
                +"</div>"
            +"</div>"
      + "</div>"
      + "<div class=\"hover-menu flex-column p-3\">"
            +"<div class=\"user-role fw-bold\">Судья</div>"
            +"<div class=\"user-name\">В. Б. Кутольвас</div>"
            +"<div class=\"user-actions flex-column mt-2\">"
                +"<a href=\"#\" class=\"user-action profile d-flex align-items-center text-decoration-none\">"
                    +"<svg class=\"me-2\" width=\"14\" height=\"15\" viewBox=\"0 0 14 15\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">"
                        +"<path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M14 13.9853L13.7938 14.9598L0.1863 15L0 14.015L4.26047 12.2656L4.44677 10.3989C4.14117 9.88914 3.90579 9.32858 3.74891 8.73688C2.49215 7.24982 2.67997 5.31316 3.34271 5.25017C3.34271 4.94052 3.33202 4.61686 3.33202 4.28096C3.33202 2.03464 4.58421 0 6.99695 0C9.40969 0 10.6161 1.96816 10.6161 4.62561C10.6161 4.8408 10.6161 5.04898 10.6161 5.25017C11.3124 5.1802 11.5659 7.08537 10.3885 8.60392C10.2678 9.28656 10.0307 9.93518 9.69066 10.5126L9.95332 12.3268L14 13.9853ZM9.06457 13.1106C9.04014 12.7694 9.00196 11.9996 8.97448 11.4451C8.59746 11.8498 8.19249 12.219 7.76353 12.549L6.47011 12.5315C6.0185 12.1984 5.59427 11.819 5.20266 11.3978C5.1767 12.0101 5.137 12.9129 5.12326 13.275C5.07897 14.4559 9.15772 14.4699 9.06457 13.1123V13.1106ZM9.81283 4.19874C9.81283 3.34036 9.51519 2.51713 8.98539 1.91017C8.45559 1.3032 7.73703 0.962212 6.98778 0.962212C6.23854 0.962212 5.51997 1.3032 4.99018 1.91017C4.46038 2.51713 4.16274 3.34036 4.16274 4.19874C4.16274 8.39748 4.60253 9.88628 6.72971 11.4661L7.45201 11.4906C9.48604 9.90728 9.81283 8.36774 9.81283 4.20049V4.19874Z\" fill=\"#000814\"/>"
                    +"</svg>"
                    +"Профиль"
                +"</a>"
                +"<a href=\"http://127.0.0.1:8000/auth/logout/\" class=\"user-action exit d-flex align-items-center text-decoration-none\">"
                    +"<svg class=\"me-2\" width=\"14\" height=\"14\" viewBox=\"0 0 14 14\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">"
                        +"<path d=\"M1.16667 14C0.855556 14 0.583333 13.8833 0.35 13.65C0.116667 13.4167 0 13.1444 0 12.8333V1.16667C0 0.855556 0.116667 0.583333 0.35 0.35C0.583333 0.116667 0.855556 0 1.16667 0H6.825V1.16667H1.16667V12.8333H6.825V14H1.16667ZM10.6167 10.4028L9.78056 9.56667L11.7639 7.58333H4.95833V6.41667H11.725L9.74167 4.43333L10.5778 3.59722L14 7.01944L10.6167 10.4028Z\" fill=\"#000814\"/>"
                    +"</svg>"
                    +"Выход"
                +"</a>"
            +"</div>"
        +"</div>"
    )
    $('.user-profile-item').click(() => {
        $('.icon-container').toggleClass("rotator");
        $('.hover-menu').toggle();
    });
}

function get_cookie(name){
    return document.cookie.split(';').some(c => {
        return c.trim().startsWith(name + '=');
    });
}

function delete_cookie(name, domain,path) {
    if( get_cookie( name ) ) {
      document.cookie = name + "=" +
        ((path) ? ";path="+path:"")+
        ((domain)?";domain="+domain:"") +
        ";expires=Thu, 01 Jan 1970 00:00:01 GMT";
    }
}

function cookieStrToObject(cookiesString){
    cookiesArray = cookiesString.split(";")
    for(i=0; i < cookiesArray.length; i++){   
        cookiesArray[i] = new Array(cookiesArray[i].split("=")[0].trim(), cookiesArray[i].split("=")[1]);
    }
    return Object.fromEntries(cookiesArray);
}
       
function set_cookie ( name, value, exp_y, exp_m, exp_d, path, domain, secure ){
    var cookie_string = name + " = " + value;
    
    if (exp_y){
        var expires = new Date ( exp_y, exp_m, exp_d );
        cookie_string += "; expires=" + expires.toGMTString();
    }
    if (path) cookie_string += "; path=" + path;
    if (domain) cookie_string += "; domain=" + domain;
    if (secure) сookie_string += "; secure";
    cookie_string += ';';
    document.cookie = cookie_string;
}

function updateCompetition(comp_id, title=null, description=null, datetime=null){
    var data = {};
    if(title) data["name"] = title;
    if(description) data["description"] = description;
    if(datetime) data["dateTimeStartCompetition"] = datetime;

    console.log(title, description, datetime);

    $.ajax({
        method: "PUT",
        url: "http://127.0.0.1:8000/api/v1/competition/" + comp_id + "/",
        contentType: 'application/json',
        data: JSON.stringify(data),
        headers:{ "Authorization": cookieStrToObject(document.cookie).Authorization  },
        success: function(msg){
            console.log(msg);
            alert("Соревнование успешно обновлено!");
            location.reload();
        },

    })
}