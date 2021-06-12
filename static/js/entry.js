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

      $.ajax({
          type: "POST",
          url: '/processing_signup',
          data: {
              firstname: $("#firstname").val(),
              lastname: $("#lastname").val(),
              email: $("#email-signup").val(),
              password: $("#password-signup").val(),
              location: $("#location").val()
          },
          success: function(response)
          {
              if (response === 'Correct') {
                alert('Great!!! You are signed up .... Please sign in to access your account. ');
                container.classList.remove("sign-up-mode"); 
              }
              else {
                  alert("Signup-Again");
              }
          },
          error: function(){
            alert("server side error");
          }
      });

  });


  $('#signin').click(function() {

      $.ajax({
          type: "POST",
          url: '/processing_signin',
          data: {
              email: $("#email-signin").val(),
              password: $("#password-signin").val(),
          },
          success: function(response)
          {
              if (response === 'Correct') {
                window.location.href = "/entry"; 
              }
              else {
                  alert("Signin-Again");
              }
          },
          error: function(){
            alert("server side error");
          }
      });

  });

  
