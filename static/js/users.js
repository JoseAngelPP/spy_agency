$(document).ready(function() {
    console.log('Hola');
    validUserForm();
});


function validateEmail(email) {
    console.log(email)
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function validatePassword(password) {  
    var pw = password;  
    console.log(password)
    //check empty password field  
    if(pw == "" || pw.length < 8 || pw.length > 15) {  
       return false;  
    }  else {
        return true;
    }
  } 

function validUserForm(){
    console.log('aaa')
    $('#id_email').change(function(e){
        e.preventDefault();
        validEmail = validateEmail($('#id_email').val()); 
        if (!validEmail){
            $( "#id_email" ).addClass( "error" );
            $( "#email_error" ).show();
        }
        else {
            $( "#id_email" ).removeClass( "error" );
            $( "#email_error" ).hide();
        }
    });

    $('#id_password').change(function(e){
        e.preventDefault();
        validPassword = validatePassword($('#id_password').val());
        if (!validPassword){
            $( "#id_password" ).addClass( "error" );
            $( "#password_error" ).show();
        }
        else {
            $( "#id_password" ).removeClass( "error" );
            $( "#password_error" ).hide();
        }

    });
}