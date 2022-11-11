
const submitForm = () =>{
    const formRegister = document.getElementById('form-register');
    const first_name = document.getElementById('first_name').value;
    const last_name = document.getElementById('last_name').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const phone_no = document.getElementById('phone_no').value;
    const password = document.getElementById('password').value;
    const password2 = document.getElementById('password2').value;
    const address = document.getElementById('address').value;
    const flash = document.getElementById('flash');

    if (!first_name ||!last_name || !username || !email || !phone_no || !password || !password2 || !address) {
        flash.innerHTML ='<div class="alert alert-danger text-uppercase">ALL FIELD IS REQUIRED</div>';
    }
    else if (password != password2){
        flash.innerHTML ='<div class="alert alert-danger text-uppercase">PASSWORD DOES NOT MATCH</div>';
    }
    else{
        formRegister.submit()
    }
}

const submitFormLogin = () =>{
    const formLogin = document.getElementById('form-login');
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const flash = document.getElementById('flash');

    if (!username || !password) {
        flash.innerHTML ='<div class="alert alert-danger text-uppercase">ALL FIELD IS REQUIRED</div>';
    }
    else{
        formLogin.submit()
    }
}


const formValid = () => {
    let replyForm = document.getElementById('reply-form');
    const message = document.getElementById('message').value;
    const reply = document.getElementById('reply');

    if (message) {
        reply.type = "submit"
        replyForm.submit();
    }
}