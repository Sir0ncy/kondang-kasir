const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("passwordInput");

togglePassword.addEventListener("click", function () {
    const type = passwordInput.type === "password" ? "text" : "password";
    passwordInput.type = type;

    this.querySelector("i").classList.toggle("bi-eye");
    this.querySelector("i").classList.toggle("bi-eye-slash");
});