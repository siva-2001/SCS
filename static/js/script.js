$(document).ready(() => {
    
    function checkAccessPermissions(){
        $.ajax({
            method: "GET",
            url: "http://127.0.0.1:8000/permission/",
            dataType : 'json',
            headers:{
                "Authorization": cookieStrToObject(document.cookie).Authorization 
            },
            success: function(data){
                console.log(data);
                if (data.isAnonymousUser || data.details == "Invalid token.") { addAnonymousUserButtons(); }
                else {
                    if(data.isOrganizer) addCreateEventButton();
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

    function addAnonymousUserButtons(){
        $(".footer-actions").append(
            "<a href=\"http://127.0.0.1:8000/loginPage/\" id=\"login-head-button\" class=\"menu-btn menu-log-in-btn p-3 me-3 d-block text-center text-decoration-none\">"
            + "Войти"
        + "</a>"
        + "<a href=\"http://127.0.0.1:8000/signupPage/\" id=\"signup-head-button\" class=\"menu-btn menu-log-in-btn p-3 d-block text-center text-decoration-none\">"
            + "Регистрация"
        + "</a>"
        )
    }

    function addCreateEventButton(){
        $(".footer-actions").append(
          "<button type=\"button\" class=\"menu-btn menu-new-event-btn p-3 d-block text-center text-decoration-none fs-5\">"
                + "Новое событие"
          + "</button>"
        )

        $('.menu-new-event-btn').click(() => {
            $('.popup-container').css("display", "flex");
        });
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
                    +"<a href=\"http://127.0.0.1:8000/logout/\" class=\"user-action exit d-flex align-items-center text-decoration-none\">"
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
        console.log(cookie_string);
        setTimeout(() => { console.log("мир"); }, 10000);
    }

// _______________________      ajax request functions       _____________________________

    function login_user_request(username, password, scrf_token){
        $.ajax({
            method: "POST",
            url: "http://127.0.0.1:8000/login/",
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
            url: "http://127.0.0.1:8000/api-token-auth/",
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
                $(location).attr('href',"http://127.0.0.1:8000/loginPage/");
            },
        });
    }

    // ____________________     ACTIONS     ____________________________________
    // _________________________________________________________________________

    checkAccessPermissions();

    if (window.location.pathname == '/logout/'){
        print("here")
        delete_cookie("Authorization")
        delete_cookie("session_id")
    }

    if (window.location.pathname == '/'){
        $.ajax({
            method: "GET",
            url: "http://127.0.0.1:8000/api/v1/testMethod",
            dataType : 'json',
            headers:{ 
                "Authorization": cookieStrToObject(document.cookie).Authorization 
            },
            success: function(data, status){
                console.log(data)
            },
        })
    }

    //      Отправляет данные для регистрации, после авторизует пользователя
    if (window.location.pathname == '/signup/'){
        let username = $('input[name=username]');
        let password1 = $('input[name=password1]');
        let password2 = $('input[name=password2]');
        let scrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

        $('#signup-btn').click((e) => {
            e.preventDefault();
            if (username.val() === "" || password1.val() === "" || password2.val() === "") alert("Заполните пустые поля");
            else if (password1.val() != password2.val()) alert("Введённые пароли не совпадают");
            else {
                sign_up_user_request(username.val(), password1.val(), scrf_token=scrf_token);

                // АВТОРИЗАЦИЯ

                $(location).attr('href',"http://127.0.0.1:8000/loginPage/");
            }
        });  

    }
//     let container = document.querySelector("#form-container");
    //      Отправляет данные для авторизации пользователя
    if (window.location.pathname == '/loginPage/'){
        let username = $('input[name=username]');
        let password = $('input[name=password]');
        let scrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

        $('#login-btn').click((e) => {
            e.preventDefault();
            if (username.val() === "" || password.val() === "") alert("Заполните пустые поля");
            else {
                get_auth_token_request(username.val(), password.val());
                login_user_request(username.val(), password.val(), scrf_token);
                // $(location).attr('href',"http://127.0.0.1:8000");
            }
        }); 
    }


    //________________________ДЛЯ СТРАНИЦЫ СОЗДАНИЯ СОРЕВНОВАНИЙ_________________________________________________________________

    if (window.location.pathname == '/createCompetition/') {
        let sportType = $('#competition-sport');
        let type = $('input[name=type]');
        let name = $('#competition-title');
        let description = $('#competition-description');
        let date = $('#competition-date');
        let regulations = $('#regulations');
        let formData = new FormData();
        let scrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

        // вставка названия файла в поле его загрузки
        regulations.change(function(){
            if (window.FormData === undefined) alert('В вашем браузере FormData не поддерживается')
            else formData.append('file', regulations[0].files[0]);

            $('.regulation-label-text').text(regulations[0].files[0].name);
        });

        //  отправка POST-запроса к API
        $('#create-competition-btn').click((e) => {

            e.preventDefault();
            if (name.val() === "" || description.val() === "" || date.val() === "") alert("Заполните пустые поля");
            else {
                $.ajax({
                    method: "POST",
                    url: "http://127.0.0.1:8000/api/v1/test",
                    dataType : 'json',
                    data: {
                        "name": name.val(),
                        "description": description.val(),
                        "dateTimeStartCompetition": date.val().toString(),
                        "sportType": sportType.val(),
                        "type": type.val(),
                        "regulations": null,
                    },
                    headers:{"X-CSRFToken": scrf_token},
                })
                    .done(function() {
                        alert('Соревнование успешно создано');
                        $(location).attr('href',"http://127.0.0.1:8000/");
                    });
            }
        });
    }

    //________________________ДЛЯ СТРАНИЦЫ СОЗДАНИЯ СПАРТАКАИД______________________________________________________________________

    if (window.location.pathname == '/createOlympics/') {
        let competitionForm = document.querySelectorAll(".competition-form");
        let container = document.querySelector("#form-container");
        let addButton = document.querySelector("#add-form");
        let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
        let competitionsContainer = document.querySelector('#competitions-container');
        let competitionFormDescription;


        hideFormHandler(true);
        editFormHandler();
        deleteFormHandler();
        let formNum = competitionForm.length - 1;
        addButton.addEventListener('click', addForm);


        function addForm(e) {
            e.preventDefault();

            let newForm = competitionForm[0].cloneNode(true); //Clone the bird form
            let formRegex = RegExp(`form-(\\d){1}-`, 'g'); //Regex to find all instances of the form number

            newForm.style.visibility = 'visible';
            newForm.style.position = 'relative';
            formNum++ //Increment the form number
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`); //Update the new form to have the correct form number
            competitionsContainer.insertBefore(newForm, null); //Insert the new form at the end of the list of forms

            let newFormFlag = true;

            hideFormHandler(newFormFlag);

            totalForms.setAttribute('value', `${formNum + 1}`); //Increment the number of total forms in the management form
        }



        function hideFormHandler(flag = false) {
            $('.save').click((e) => {
                let target = $(e.target).parent().parent();
                if (target.hasClass('competition-form')) {
                    target.css("visibility", "hidden");
                    target.css("position", "absolute");
                    console.log(competitionForm[0]);
                    // addFormItem(target.parent(), flag);
                } else if (target.parent().hasClass('competition-form')) {
                    target.parent().css("visibility", "hidden");
                    target.parent().css("position", "absolute");
                    // addFormItem(target.parent().parent(), flag);
                } else {
                    target.parent().parent().css("visibility", "hidden");
                    target.parent().parent().css("position", "absolute");
                    // addFormItem(target.parent().parent().parent(), flag);
                }
            });
        }



        function addFormItem(target, flag) {
            if (flag) {
                target.append("<div class=\"competition-item col-8 mb-4 p-4\">\n" +
                    "                     <div class=\"competition-title form-label text-white\">Соревнования по" + ' ' + target.children('#competition-sport').text() + "</div>\n" +
                    "                     <div class=\"competition-description text-white fs-5 pb-4\">" + target.children('.competition-description').text() + "</div>\n" +
                    "                     <div class=\"competition-type-and-date text-white fs-5\">межвузовские, 22.09.2022</div>\n" +
                    "                     <div class=\"competition-actions\">\n" +
                    "                         <button class=\"competition-btn edit\">\n" +
                    "                             <svg width=\"15\" height=\"17\" viewBox=\"0 0 15 17\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
                    "                                 <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M12.7768 5.45492L9.11011 2.30155C9.71072 1.59296 10.1911 1.0516 10.4607 0.781291C11.97 -0.694608 15.4261 2.19285 13.8805 4.08791C13.6701 4.34981 13.2804 4.83233 12.7768 5.45492ZM4.80103 15.3505L0.418509 16.7293L1.20088 12.0983C1.20088 12.0983 5.33845 6.84414 8.15157 3.43764L11.8375 6.60684C9.1039 10.0025 4.80103 15.3505 4.80103 15.3505Z\" fill=\"white\"/>\n" +
                    "                             </svg>\n" +
                    "                         </button>\n" +
                    "                         <button class=\"competition-btn delete\">\n" +
                    "                             <svg width=\"19\" height=\"20\" viewBox=\"0 0 19 20\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
                    "                                 <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M19 16.0885V18.079L17.0732 19.7819L12.9084 19.8399L12.322 18.4479L11.2688 17.5895L11.568 14.2417H12.9036L14.5288 12.4275L18.2245 13.5875L18.1646 15.534L19 16.0885ZM14.9597 13.7476L13.94 14.6756L14.682 15.1396L16.3432 14.2116L14.9597 13.7476ZM17.6309 16.5316L15.7017 15.6175L14.6796 16.1859L13.2435 15.5943L12.3986 17.3923L15.1512 17.3529L15.6107 18.4618L16.4628 18.666L17.0062 17.6521L17.9061 17.4967L17.6309 16.5316ZM0 4.05221L14.5073 3.88749L14.56 6.56943L0.241749 6.4743L0 4.05221ZM8.58806 2.8922V1.94331L5.82351 1.91083V2.87364H3.85362C3.85362 2.87364 3.80814 2.16371 3.79617 1.58835C3.76984 0.535062 4.42328 0.0455384 5.66075 0.0060981C6.24717 -0.0147821 7.99924 0.0246578 8.73406 0.0246578C10.0673 0.0246578 10.5915 0.535062 10.5986 1.38187C10.5986 1.96883 10.5532 2.90612 10.5532 2.90612L8.58806 2.8922ZM13.6145 11.8103L11.4962 13.2024C11.5752 11.8846 11.6446 10.6875 11.6781 10.1631C11.7595 8.79896 10.0338 8.88016 10.0385 10.1214C10.0385 10.7803 10.0649 15.8031 10.0721 17.5454H10.1558L10.1008 18.2066L11.4005 19.8306L1.63479 20L1.20156 7.65519H13.7773L13.6145 11.8103ZM3.42996 10.2188C3.42996 10.9635 3.60469 16.571 3.64777 17.8981L5.00013 17.8238C5.01688 16.5989 5.09587 11.2141 5.09587 10.1539C5.0839 8.85696 3.42996 8.83608 3.42996 10.2188ZM6.78093 10.2026C6.85991 10.9125 6.93651 16.114 6.95805 17.7148L8.35349 17.6382C8.37742 15.9493 8.44684 11.2535 8.44684 10.1376C8.45641 8.77112 6.64689 8.97064 6.78093 10.2026Z\" fill=\"white\"/>\n" +
                    "                             </svg>\n" +
                    "                         </button>\n" +
                    "                     </div>\n" +
                    "                 </div>");
                editFormHandler();
                deleteFormHandler();
            }
        }

        function editFormHandler() {
            $('.edit').click((e) => {
                let target = $(e.target).parent().parent();
                if (target.hasClass('competition-item')) {
                    target.prev().css("visibility", "visible");
                    target.prev().css("position", "relative");
                    target.remove();
                } else if (target.parent().hasClass('competition-item')) {
                    target.parent().prev().css("visibility", "visible");
                    target.parent().prev().css("position", "relative");
                    target.parent().remove();
                } else {
                    target.parent().parent().prev().css("visibility", "visible");
                    target.parent().parent().prev().css("position", "relative");
                    target.parent().parent().remove();
                }
            });
        }

        function deleteFormHandler() {
            $('.delete').click((e) => {
                let target = $(e.target).parent().parent();
                if (target.hasClass('competition-item')) {
                    target.prev().remove();
                    target.remove();
                } else if (target.parent().hasClass('competition-item')) {
                    target.parent().prev().remove();
                    target.parent().remove();
                } else {
                    target.parent().parent().prev().remove();
                    target.parent().parent().remove();
                }
            });
        }


    }




    
    // добавление имени файла при загружке в поле

    /*let fileInput = $('#regulations');

    if(fileInput.length > 1){
        console.log("no files selected");
    } else {
        // $('.regulation-label-text').text('Выбранный файл ' + fileInput.value);
        console.log(fileInput.length);
    }*/

    /*$('.add-competition-button').click(() => {
        $('.competitions').prepend("<div class=\"competition-form mb-4 col-8 p-4\">\n" +
            "                        <div class=\"competition-actions\">\n" +
            "                            <button type=\"button\" class=\"competition-btn save\">\n" +
            "                                <svg width=\"26\" height=\"19\" viewBox=\"0 0 26 19\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
            "                                    <path d=\"M10.2304 16.5751L23.5084 3.65165L22.248 2.42493L10.2304 14.1216L4.04577 8.1021L2.78539 9.32883L10.2304 16.5751ZM10.2304 19L0.293945 9.32883L4.04577 5.67718L10.2304 11.6967L22.248 0L25.9998 3.65165L10.2304 19Z\" fill=\"white\"/>\n" +
            "                                    <rect x=\"4.20776\" y=\"7.12744\" width=\"11.7183\" height=\"2.72692\" transform=\"rotate(45.6413 4.20776 7.12744)\" fill=\"white\"/>\n" +
            "                                    <rect x=\"24.1638\" y=\"3.0437\" width=\"19.0052\" height=\"2.1078\" transform=\"rotate(135 24.1638 3.0437)\" fill=\"white\"/>\n" +
            "                                </svg>\n" +
            "                            </button>\n" +
            "                        </div>\n" +
            "                        <div class=\"row d-flex justify-content-center\">\n" +
            "                            <div class=\"mb-3 col-5\">\n" +
            "                                <label class=\"form-label text-white\">Вид спорта</label>\n" +
            "                                {{ form.competitions.0.sportType }}\n" +
            "                            </div>\n" +
            "                            <div class=\"mb-3 col-5\">\n" +
            "                                <label class=\"form-label text-white\">Дата начала</label>\n" +
            "                                {{ form.competitions.0.dateTimeStartCompetition }}\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                        <div class=\"row d-flex justify-content-center\">\n" +
            "                            <div class=\" col-10 mb-3\">\n" +
            "                                <label class=\"form-label text-white\">Короткое описание</label>\n" +
            "                                {{ form.competitions.0.description }}\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                        <div class=\"row d-flex justify-content-center\">\n" +
            "                            <div class=\"col-10 mb-3\">\n" +
            "                                <label class=\"form-label text-white\">Загрузить регламент</label>\n" +
            "                                <div class=\"dashed-block white-dashed-block mb-0 p-5 text-center\">\n" +
            "                                    <svg width=\"88\" height=\"64\" viewBox=\"0 0 88 64\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
            "                                        <path fill-rule=\"evenodd\" clip-rule=\"evenodd\"\n" +
            "                                              d=\"M63.5269 64H46.8172L46.3478 35.6595L53.3393 41.501L56.875 36.8121L42.5824 25.3853L29.3585 36.9894L32.7244 41.6094L39.9056 35.8861L40.0055 63.9507C32.0153 63.9507 24.2947 63.9507 18.242 63.9507C-3.49149 63.9507 -5.91853 35.2163 11.5702 28.9906C11.4703 14.5495 20.9088 0 40.0654 0C54.0484 0 63.1373 7.6934 67.0326 17.4357C95.3781 20.2432 95.7276 64 63.5269 64Z\"\n" +
            "                                              fill=\"#ffffff\"/>\n" +
            "                                    </svg>\n" +
            "                                    <label class=\"regulation-label\">\n" +
            "                                        <span class=\"regulation-label-text text-center d-block\">Нажмите или перетащите файл, чтобы загрузить регламент</span>\n" +
            "                                        {{ form.competitions.0.regulations }}\n" +
            "                                    </label>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                    </div>");
    });
    $('.save').click(() => {

    });*/
    
});