document.addEventListener("DOMContentLoaded", () => {
    new ClipboardJS(".copy-btn", {
        text: function(trigger) {
            var uuid = trigger.getAttribute("data-uuid")
            return window.location.origin + "/exam/notice?data=" + uuid;
        }
    });

    $('.copy-btn').popover({
        trigger: 'focus',
        delay: { "show": 0, "hide": 1000 }
    });


    var archive_form = document.getElementsByClassName("archive-form");


    for(var i=0; i < archive_form.length; i++){
        archive_form[i].addEventListener("submit", (e) => {
            e.preventDefault();
            const csrf_token = Cookies.get('csrftoken');
            const key = e.target.getAttribute("data-uuid");
            const url = window.location.href;
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': "application/json",
                    'X-CSRFToken': csrf_token,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({
                    'key': key
                })
            };            
            
            fetch(url, options)
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    location.reload();
                });

        });
    }
    

})

