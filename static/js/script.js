$(document).ready(() => {
    checkAccessPermissions();

    if (window.location.pathname == '/logout/'){
        print("here")
        delete_cookie("Authorization")
        delete_cookie("session_id")
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
        let formData = new FormData();

        $('#regulations').change(function(){
            if (window.FormData === undefined) alert('В вашем браузере FormData не поддерживается, что приведёт к ошибкам при загрузке файла регламента');
            $('.regulation-label-text').text($('#regulations')[0].files[0].name);
        });

        $('#create-competition-btn').click((e) => {
            e.preventDefault();

            formData.append('name', $('#competition-title').val());
            formData.append('description', $('#competition-description').val());
            formData.append('dateTimeStartCompetition', $('#competition-date').val().toString());
            formData.append('sportType', $('#competition-sport').val());
            formData.append('type', $('input[name=type]').val());
            formData.append('regulations', $('#regulations')[0].files[0]);

            if ($('#competition-title').val() === "" 
                || $('#competition-description').val() === "" 
                || $('#competition-date').val() === "") alert("Заполните пустые поля");
            else {
                $.ajax({
                    method: "POST",
                    url: "http://127.0.0.1:8000/api/v1/competitions/",
                    dataType : 'json',
                    contentType: false,
                    processData: false,
                    cache: false,
                    data: formData,
                    headers:{
                        "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').attr('value'),
                        "Authorization": cookieStrToObject(document.cookie).Authorization 
                    },
                })
                .done(function() {
                    alert('Соревнование успешно создано');
                    $(location).attr('href',"http://127.0.0.1:8000/");
                });
            }
        });
    }

    //________________________ДЛЯ СТРАНИЦЫ СОЗДАНИЯ СПАРТАКАИД______________________________________________________________________

    // if (window.location.pathname == '/createOlympics/') {
    //     let competitionForm = document.querySelectorAll(".competition-form");
    //     let container = document.querySelector("#form-container");
    //     let addButton = document.querySelector("#add-form");
    //     let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
    //     let competitionsContainer = document.querySelector('#competitions-container');
    //     let competitionFormDescription;


    //     hideFormHandler(true);
    //     editFormHandler();
    //     deleteFormHandler();
    //     let formNum = competitionForm.length - 1;
    //     addButton.addEventListener('click', addForm);


    //     function addForm(e) {
    //         e.preventDefault();

    //         let newForm = competitionForm[0].cloneNode(true); //Clone the bird form
    //         let formRegex = RegExp(`form-(\\d){1}-`, 'g'); //Regex to find all instances of the form number

    //         newForm.style.visibility = 'visible';
    //         newForm.style.position = 'relative';
    //         formNum++ //Increment the form number
    //         newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`); //Update the new form to have the correct form number
    //         competitionsContainer.insertBefore(newForm, null); //Insert the new form at the end of the list of forms

    //         let newFormFlag = true;

    //         hideFormHandler(newFormFlag);

    //         totalForms.setAttribute('value', `${formNum + 1}`); //Increment the number of total forms in the management form
    //     }



    //     function hideFormHandler(flag = false) {
    //         $('.save').click((e) => {
    //             let target = $(e.target).parent().parent();
    //             if (target.hasClass('competition-form')) {
    //                 target.css("visibility", "hidden");
    //                 target.css("position", "absolute");
    //                 console.log(competitionForm[0]);
    //                 // addFormItem(target.parent(), flag);
    //             } else if (target.parent().hasClass('competition-form')) {
    //                 target.parent().css("visibility", "hidden");
    //                 target.parent().css("position", "absolute");
    //                 // addFormItem(target.parent().parent(), flag);
    //             } else {
    //                 target.parent().parent().css("visibility", "hidden");
    //                 target.parent().parent().css("position", "absolute");
    //                 // addFormItem(target.parent().parent().parent(), flag);
    //             }
    //         });
    //     }



    //     function addFormItem(target, flag) {
    //         if (flag) {
    //             target.append("<div class=\"competition-item col-8 mb-4 p-4\">\n" +
    //                 "                     <div class=\"competition-title form-label text-white\">Соревнования по" + ' ' + target.children('#competition-sport').text() + "</div>\n" +
    //                 "                     <div class=\"competition-description text-white fs-5 pb-4\">" + target.children('.competition-description').text() + "</div>\n" +
    //                 "                     <div class=\"competition-type-and-date text-white fs-5\">межвузовские, 22.09.2022</div>\n" +
    //                 "                     <div class=\"competition-actions\">\n" +
    //                 "                         <button class=\"competition-btn edit\">\n" +
    //                 "                             <svg width=\"15\" height=\"17\" viewBox=\"0 0 15 17\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
    //                 "                                 <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M12.7768 5.45492L9.11011 2.30155C9.71072 1.59296 10.1911 1.0516 10.4607 0.781291C11.97 -0.694608 15.4261 2.19285 13.8805 4.08791C13.6701 4.34981 13.2804 4.83233 12.7768 5.45492ZM4.80103 15.3505L0.418509 16.7293L1.20088 12.0983C1.20088 12.0983 5.33845 6.84414 8.15157 3.43764L11.8375 6.60684C9.1039 10.0025 4.80103 15.3505 4.80103 15.3505Z\" fill=\"white\"/>\n" +
    //                 "                             </svg>\n" +
    //                 "                         </button>\n" +
    //                 "                         <button class=\"competition-btn delete\">\n" +
    //                 "                             <svg width=\"19\" height=\"20\" viewBox=\"0 0 19 20\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
    //                 "                                 <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M19 16.0885V18.079L17.0732 19.7819L12.9084 19.8399L12.322 18.4479L11.2688 17.5895L11.568 14.2417H12.9036L14.5288 12.4275L18.2245 13.5875L18.1646 15.534L19 16.0885ZM14.9597 13.7476L13.94 14.6756L14.682 15.1396L16.3432 14.2116L14.9597 13.7476ZM17.6309 16.5316L15.7017 15.6175L14.6796 16.1859L13.2435 15.5943L12.3986 17.3923L15.1512 17.3529L15.6107 18.4618L16.4628 18.666L17.0062 17.6521L17.9061 17.4967L17.6309 16.5316ZM0 4.05221L14.5073 3.88749L14.56 6.56943L0.241749 6.4743L0 4.05221ZM8.58806 2.8922V1.94331L5.82351 1.91083V2.87364H3.85362C3.85362 2.87364 3.80814 2.16371 3.79617 1.58835C3.76984 0.535062 4.42328 0.0455384 5.66075 0.0060981C6.24717 -0.0147821 7.99924 0.0246578 8.73406 0.0246578C10.0673 0.0246578 10.5915 0.535062 10.5986 1.38187C10.5986 1.96883 10.5532 2.90612 10.5532 2.90612L8.58806 2.8922ZM13.6145 11.8103L11.4962 13.2024C11.5752 11.8846 11.6446 10.6875 11.6781 10.1631C11.7595 8.79896 10.0338 8.88016 10.0385 10.1214C10.0385 10.7803 10.0649 15.8031 10.0721 17.5454H10.1558L10.1008 18.2066L11.4005 19.8306L1.63479 20L1.20156 7.65519H13.7773L13.6145 11.8103ZM3.42996 10.2188C3.42996 10.9635 3.60469 16.571 3.64777 17.8981L5.00013 17.8238C5.01688 16.5989 5.09587 11.2141 5.09587 10.1539C5.0839 8.85696 3.42996 8.83608 3.42996 10.2188ZM6.78093 10.2026C6.85991 10.9125 6.93651 16.114 6.95805 17.7148L8.35349 17.6382C8.37742 15.9493 8.44684 11.2535 8.44684 10.1376C8.45641 8.77112 6.64689 8.97064 6.78093 10.2026Z\" fill=\"white\"/>\n" +
    //                 "                             </svg>\n" +
    //                 "                         </button>\n" +
    //                 "                     </div>\n" +
    //                 "                 </div>");
    //             editFormHandler();
    //             deleteFormHandler();
    //         }
    //     }

    //     function editFormHandler() {
    //         $('.edit').click((e) => {
    //             let target = $(e.target).parent().parent();
    //             if (target.hasClass('competition-item')) {
    //                 target.prev().css("visibility", "visible");
    //                 target.prev().css("position", "relative");
    //                 target.remove();
    //             } else if (target.parent().hasClass('competition-item')) {
    //                 target.parent().prev().css("visibility", "visible");
    //                 target.parent().prev().css("position", "relative");
    //                 target.parent().remove();
    //             } else {
    //                 target.parent().parent().prev().css("visibility", "visible");
    //                 target.parent().parent().prev().css("position", "relative");
    //                 target.parent().parent().remove();
    //             }
    //         });
    //     }

    //     function deleteFormHandler() {
    //         $('.delete').click((e) => {
    //             let target = $(e.target).parent().parent();
    //             if (target.hasClass('competition-item')) {
    //                 target.prev().remove();
    //                 target.remove();
    //             } else if (target.parent().hasClass('competition-item')) {
    //                 target.parent().prev().remove();
    //                 target.parent().remove();
    //             } else {
    //                 target.parent().parent().prev().remove();
    //                 target.parent().parent().remove();
    //             }
    //         });
    //     }


    // }




    
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