password1=document.getElementById("id_password1");
username=document.getElementById("id_username");
guidelines=document.getElementById("password-guidelines");
password1.addEventListener("focus",()=>{
    guidelines.style.display='block';
})
password1.addEventListener("blur",()=>{
    guidelines.style.display='none';
})
password1.addEventListener("input",()=>{
    const lengthcheck=document.getElementById("length-check");
    const capitalcheck=document.getElementById("capital-check");
    const numbercheck=document.getElementById("number-check");
    const matchcheck=document.getElementById("match-check");
    const userVal = username.value.toLowerCase();
    const passVal = password1.value.toLowerCase();
    if (password1.value.length >= 8) {
        lengthcheck.classList.add('is-valid')
    } else {
        lengthcheck.classList.remove('is-valid')
    }
    if (/[A-Z]/.test(password1.value)) {
        capitalcheck.classList.add('is-valid')
    } else {
       capitalcheck.classList.remove('is-valid')
    }
    if (/[0-9]/.test(password1.value)) {
        numbercheck.classList.add('is-valid')
    } else {
        numbercheck.classList.remove('is-valid')
    }
    if (passVal === "" || (userVal !== "" && passVal.includes(userVal))) {
        matchcheck.classList.remove('is-valid')
    } else {
        matchcheck.classList.add('is-valid')
    }
 

})