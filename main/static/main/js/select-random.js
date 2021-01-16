document.addEventListener("DOMContentLoaded", () => {
    var randomize_btn = document.getElementById("randomize-btn");

    var section_one = document.getElementById("div_id_questions_one").getElementsByTagName("input");
    var section_two = document.getElementById("div_id_questions_two").getElementsByTagName("input");



    function select_random_checkboxes(input_group, section_limit){
        for(var i=0; i<input_group.length; i++){
            input_group[i].checked = false;
        }

        for(var i=0; i<section_limit;i++){
            var random_select = Math.floor(Math.random()*input_group.length);
            while(input_group[random_select].checked == true){
                random_select = Math.floor(Math.random()*input_group.length);
            }
            input_group[random_select].checked = true;
        }
    }

    randomize_btn.addEventListener("click", (e) => {
        
        select_random_checkboxes(section_one, 15);
        select_random_checkboxes(section_two, 2);


    });
});