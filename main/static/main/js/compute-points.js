document.addEventListener("DOMContentLoaded", () => {

    var inputs = document.getElementsByClassName("point-input")


    function get_points(inputs){
        var total_points = 0
        for(var i =0; i<inputs.length;i++){
            total_points += parseInt(inputs[i].value);
        }
        document.getElementById("total_points").value = total_points;
        document.getElementById("total_points").innerHTML = total_points;
    }

    function get_final_grade(){
        var total_points = 0;
        var inputs = document.getElementsByClassName("compute-final");
        for(var i=0;i<inputs.length;i++){
            total_points += parseInt(inputs[i].innerHTML);
        }
        document.getElementById("final-grade").innerHTML = "Final grade: " + total_points;
        document.getElementById("final-grade-input").value = total_points;

    }

    

    if(inputs.length != 0){
        for(var i=0;i<inputs.length;i++){
            get_points(inputs);
            get_final_grade();
            inputs[i].addEventListener("input", (e) => {
                get_points(inputs);
                get_final_grade();
    
            });
        }    
    } else {
        document.getElementById("total_points").value = 0;
        document.getElementById("total_points").innerHTML = 0;
        get_final_grade();
    }

});