const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

  if ((window.location.href).includes("signup")){
  container.classList.add("sign-up-mode");
  }

  $('#signup').click(function() {
    var user_info = {
              firstname: $("#firstname").val(),
              lastname: $("#lastname").val(),
              email: $("#email-signup").val(),
              password: $("#password-signup").val(),
              location: $("#location").val()
          }


      $.ajax({
          url: '/processing_signup',
          type: "POST",
          data: JSON.stringify(user_info),
          dataType: "json",
          contentType: 'application/json',
          success: function(response) {
            if (response.resp1 === 'Correct') {
              if (response.resp2 === 'Registered'){
                alert('Great!!! You are signed up .... Please sign in to access your account. ');
                container.classList.remove("sign-up-mode");
                }
              else{
                alert(response.resp2)

              }

            }
            else {
              alert("Server did not respond");
            }
          },
          error: function(){
            alert("server side error");
          }
      });   

  });



  $('#signin').click(function() {
    var user_signin={
              email: $("#email-signin").val(),
              password: $("#password-signin").val(),
          }
      $.ajax({
          type: "POST",
          url: '/processing_signin',
          data: JSON.stringify(user_signin),
          dataType: "json",
          contentType: 'application/json',
          success: function(response)
          {
              if (response.resp1 === 'Correct') {
                //console.log("done")
                window.location.href = response.resp2; 
              }
              else {
                  alert(response.resp2);
              }
          },
          error: function(){
            alert("server side error");
          }
      });

  });

  
