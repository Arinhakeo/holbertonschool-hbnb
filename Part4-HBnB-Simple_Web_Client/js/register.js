document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    const errorMessage = document.getElementById('register-error');

    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Récupération des valeurs du formulaire
        const formData = new FormData(registerForm);
        const userData = Object.fromEntries(formData.entries());

        // Validation du mot de passe
        if (userData.password !== userData.confirmPassword) {
            errorMessage.textContent = "Les mots de passe ne correspondent pas";
            return;
        }

        try {
            // Appel à votre API d'inscription
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            if (response.ok) {
                // Redirection vers la page de connexion après inscription réussie
                window.location.href = 'login.html';
            } else {
                const data = await response.json();
                errorMessage.textContent = data.message || "Une erreur est survenue lors de l'inscription";
            }
        } catch (error) {
            errorMessage.textContent = "Une erreur est survenue lors de l'inscription";
            console.error('Erreur:', error);
        }
    });
});