const password1 = document.getElementById("id_password1");
const guidelines = document.getElementById("password-guidelines");

const lengthCheck = document.getElementById("length-check");
const capitalCheck = document.getElementById("capital-check");
const numberCheck = document.getElementById("number-check");

password1.addEventListener("focus", () => {
    guidelines.style.display = "block";
});

password1.addEventListener("blur", () => {
    guidelines.style.display = "none";
});

password1.addEventListener("input", () => {
    const value = password1.value;

    lengthCheck.classList.toggle("is-valid", value.length >= 8);
    capitalCheck.classList.toggle("is-valid", /[A-Z]/.test(value));
    numberCheck.classList.toggle("is-valid", /[0-9]/.test(value));
});