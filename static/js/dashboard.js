/*===== SHOW NAVBAR  =====*/ 
const showNavbar = (toggleId, navId, bodyId, headerId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)

    // Validate that all variables exist
    if(toggle && nav && bodypd && headerpd){
        toggle.addEventListener('click', ()=>{
            // show navbar
            nav.classList.toggle('show')
            // change icon
            toggle.classList.toggle('bx-x')
            // add padding to body
            bodypd.classList.toggle('body-pd')
            // add padding to header
            headerpd.classList.toggle('body-pd')
        })
    }
}

showNavbar('header-toggle','nav-bar','body-pd','header')

/*===== LINK ACTIVE  =====*/ 
const linkColor = document.querySelectorAll('.nav__link')

function colorLink(){
    if(linkColor){
        linkColor.forEach(l=> l.classList.remove('active'))
        this.classList.add('active')
    }
}
linkColor.forEach(l=> l.addEventListener('click', colorLink))



$("#next1").click(function() {
    var user_info={
        bus:$('#bus-points').val(),
        metro:$('#metro-points').val(),
        train:$('#train-points').val(),
        car:$('#car-points').val(),
        bike:$('#bike-points').val(),
        bicycle:$('#bicycle-points').val(),
        walking:$('#walking-points').val(),
        hour:$('#hour-quantity').val(),
        minute:$('#min-quantity').val(),
        food:$('input[name=example1]:checked', '#form2').val(),
    };

    console.log(user_info);
    $.ajax({
        type: "POST",
        url: '/questionare_update',
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