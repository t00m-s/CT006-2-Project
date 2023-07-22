$(document).ready(function () {
    mostraPassword();
})

function mostraPassword() {
    const togglePassword = document.querySelector("#togglePassword");
    const password = document.querySelector("#user_password");

    togglePassword.addEventListener("click", function () {
        // toggle the type attribute
        const type = password.getAttribute("type") === "password" ? "text" : "password";
        password.setAttribute("type", type);

        // toggle the icon
        this.classList.toggle("bi-eye");
    });

    const togglePassword_2 = document.querySelector("#togglePassword_2");
    const password_2 = document.querySelector("#user_password_2");

    togglePassword_2.addEventListener("click", function () {
        // toggle the type attribute
        const type_2 = password_2.getAttribute("type") === "password" ? "text" : "password";
        password_2.setAttribute("type", type_2);

        // toggle the icon
        this.classList.toggle("bi-eye");
    });
}

