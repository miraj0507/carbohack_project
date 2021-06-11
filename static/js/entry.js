const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});



  $('#signup').click(function() {

      $.ajax({
          type: "POST",
          url: 'admin/login.php',
          data: {
              'fullname': $("#fullname").val(),
              'email': $("#email-signup").val(),
              'password': $("#password-signup").val(),
              'location': $("#location").val()
          },
          success: function(data)
          {
              if (data === 'Correct') {
                container.classList.remove("sign-up-mode");
              }
              else {
                  alert("Signup-Again");
              }
          },
          error: function(){
            alert("signup-again");
          }
      });

  });

  
