$(document).ready(() => {

    // добавление имени файла при загружке в поле

    /*let fileInput = $('#regulations');

    if(fileInput.length > 1){
        console.log("no files selected");
    } else {
        // $('.regulation-label-text').text('Выбранный файл ' + fileInput.value);
        console.log(fileInput.length);
    }*/

    $('.add-competition-button').click(() => {
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

    });
});