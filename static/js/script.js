$(document).ready(() => {

    let fileInput = $('#regulations');

    if(fileInput.length > 1){
        console.log("no files selected");
    } else {
        // $('.regulation-label-text').text('Выбранный файл ' + fileInput.value);
        console.log(fileInput.length);
    }
});