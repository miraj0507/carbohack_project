           
var form1= document.getElementById("form1");
var form2= document.getElementById("form2");
var form3= document.getElementById("form3");

var next1= document.getElementById("next1");
var next2= document.getElementById("next2");
var back1= document.getElementById("back1");
var back2= document.getElementById("back2");
var progress= document.getElementById("progress");
next1.onclick=function(){
    form1.style.left="-1510px";
    form2.style.left="1px";
    progress.style.width="66%";
}
back1.onclick=function(){
    form1.style.left="1px";
    form2.style.left="1510px";
    progress.style.width="33%";
}
next2.onclick=function(){
    form2.style.left="-1510px";
    form3.style.left="1px";
    progress.style.width="100%";
}
back2.onclick=function(){
    form2.style.left="1px";
    form3.style.left="1510px";
    progress.style.width="66%";
}



var rangeSlider = document.getElementById("range-slider");
var waoo = document.getElementById("waoo");

var rangeLabel = document.getElementById("range-label");

rangeSlider.addEventListener("input", showSliderValue);

function showSliderValue() {
  waoo.innerHTML = rangeSlider.value;
  var labelPosition = (rangeSlider.value /rangeSlider.max);
  
  if(rangeSlider.value === rangeSlider.min) {
 rangeLabel.style.left = ((labelPosition * 100) + 2) + "%";
  } else if (rangeSlider.value === rangeSlider.max) {
 rangeLabel.style.left = ((labelPosition * 100) - 2) + "%";
  } else {
  rangeLabel.style.left = (labelPosition * 100) + "%";
  }
}

$("#final-submit").click(function() {
    var user_info={
        bus:$('#step1-bus').val(),
        metro:$('#step1-metro').val(),
        train:$('#step1-train').val(),
        car:$('#step1-car').val(),
        bike:$('#step1-bike').val(),
        bicycle:$('#step1-bicycle').val(),
        walking:$('#step1-walking').val(),
        hour:$('#step1-hour').val(),
        minute:$('#step1-min').val(),
        food:$('input[name=example1]:checked', '#form2').val(),
        elec_bill:$('#range-slider').val(),
        no_of_member:$('#member-quantity').val(),
        elec_bill:$('#range-slider').val(),
        flights:$('#flight').val(),
        state:$('#state').val()
    };

    console.log(user_info);
    $.ajax({
        type: "POST",
        url: '/questionare_filling',
        data: JSON.stringify(user_info),
        dataType: "json",
        contentType: 'application/json',
        success: function(response)
        {
            if (response.resp1 === 'Correct') {
              if (response.resp2 === 'Registered'){
                window.location.href = '/MyAccount';
              }
              else{
                  alert(response.resp2);
              }
            }
            else {
                alert("No response from server");
            }
        },
        error: function(){
          alert("server side error");
        }
    });
});