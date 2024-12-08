document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('login-error');

    loginForm.addEventListener('submit', function(event) {
        let isValid = true;
        let message = '';

        if (!emailInput.value.includes('@')) {
            isValid = false;
            message += 'Veuillez entrer une adresse e-mail valide.\n';
        }

        if (passwordInput.value.length < 6) {
            isValid = false;
            message += 'Le mot de passe doit contenir au moins 6 caractères.\n';
        }

        if (!isValid) {
            event.preventDefault();
            errorMessage.textContent = message;
        }
    });
});