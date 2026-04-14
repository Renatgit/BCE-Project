document.getElementById("showPassword").addEventListener("change", function() {
    const passwordField = document.getElementById("password");
    const confirmField = document.getElementById("confirm_password");

    if (this.checked) {
        passwordField.type = "text";
        confirmField.type = "text";
    } else {
        passwordField.type = "password";
        confirmField.type = "password";
    }
});