document.addEventListener("DOMContentLoaded", () => {
    var inputs = document.getElementsByTagName("input");
    
    for(var i=0; i<inputs.length;i++){

        if(inputs[i].name != "csrfmiddlewaretoken"){

            inputs[i].checked = Cookies.get(inputs[i].value);

            inputs[i].addEventListener('click', (e) => {
                if(e.target.checked == true){
                    Cookies.set("URL", document.location.href, { sameSite: 'strict' });
                    Cookies.set(e.target.value, true, { sameSite: 'strict' });
                } else {
                    Cookies.remove(e.target.value, { sameSite: 'strict' });
                }
            });
        }
    }

});