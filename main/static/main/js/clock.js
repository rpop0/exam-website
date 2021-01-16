$(document).ready(function(){
    console.log("bepis");
    clockUpdate();
    getDate();
    setInterval(clockUpdate, 1000);
});

function clockUpdate() {
    var date = new Date();
    function addZero(x) {
        if (x < 10) {
        return x = '0' + x;
        } else {
        return x;
        }
    }

    var h = addZero(date.getHours());
    var m = addZero(date.getUTCMinutes());
    var s = addZero(date.getUTCSeconds());

    $('.digital-clock').text(h + ':' + m + ':' + s)
    $('.digital-clock').removeClass("hidden");
}

function getDate(){
    var date = new Date()

    var month = date.getUTCMonth();
    var day = date.getUTCDate();
    var year = date.getUTCFullYear();
    switch(month){
        case 0:
            month = "JAN";
            break;
        case 1:
            month = "FEB";
            break;
        case 2:
            month = "MAR";
            break;
        case 3:
            month = "APR";
            break;
        case 4:
            month = "MAY";
            break;
        case 5:
            month = "JUN";
            break;
        case 6:
            month = "JUL";
            break;
        case 7:
            month = "AUG";
            break;
        case 8:
            month = "SEP";
            break;
        case 9:
            month = "OCT";
            break;
        case 10:
            month  = "NOV";
            break;
        case 11:
            month = "DEC";
            break;
    }
    $('.clock-date').text(day + '/' + month + '/' + year);
    $('.clock-date').removeClass("hidden");
}