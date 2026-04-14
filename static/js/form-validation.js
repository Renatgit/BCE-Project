//GET ELEMENTS
const form = document.querySelector(".reg-form");

const emailInput = document.getElementById("email");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const confirmInput = document.getElementById("confirm_password");

const emailError = document.getElementById("email-error");
const usernameError = document.getElementById("username-error");
const confirmError = document.getElementById("confirm-error");
const passwordError = document.getElementById("password-error");

//EMAIL VALIDATION
emailInput.addEventListener("input", () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(emailInput.value)) {
        emailError.textContent = "Invalid email format";
    } else {
        emailError.textContent = "";
    }
});

//USERNAME VALIDATION
usernameInput.addEventListener("input", () => {
    if (usernameInput.value.length < 3) {
        usernameError.textContent = "Username must be at least 3 characters";
    } else {
        usernameError.textContent = "";
    }
});

//PASSWORD LENGTH
passwordInput.addEventListener("input", () => {
    if (passwordInput.value.length < 8) {
        passwordError.textContent = "Password must be at least 8 characters";
    } else {
        passwordError.textContent = "";
    }
});

//PASSWORD MATCH
confirmInput.addEventListener("input", () => {
    if (confirmInput.value !== passwordInput.value) {
        confirmError.textContent = "Passwords do not match";
    } else {
        confirmError.textContent = "";
    }
});

//CHECK EMAIL EXISTS
emailInput.addEventListener("blur", async () => {
    if (!emailInput.value) return;

    const res = await fetch(`/check_user?email=${emailInput.value}`);
    const data = await res.json();

    if (data.emailExists) {
        emailError.textContent = "Email already exists";
    }
});

//CHECK USERNAME EXISTS
usernameInput.addEventListener("blur", async () => {
    if (!usernameInput.value) return;

    const res = await fetch(`/check_user?username=${usernameInput.value}`);
    const data = await res.json();

    if (data.usernameExists) {
        usernameError.textContent = "Username already taken";
    }
});

//FINAL SUBMIT CHECK
form.addEventListener("submit", function(e) {

    if (
        emailError.textContent ||
        usernameError.textContent ||
        passwordError.textContent ||
        confirmError.textContent
    ) {
        e.preventDefault();
        alert("Please fix errors before submitting");
    }

});
