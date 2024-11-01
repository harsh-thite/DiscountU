// script.js
document.addEventListener("DOMContentLoaded", () => {
    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    const loginBtn = document.getElementById("loginBtn");
    const registerBtn = document.getElementById("registerBtn");

    const loginClose = document.getElementById("loginClose");
    const registerClose = document.getElementById("registerClose");

    // Open login modal
    loginBtn.onclick = () => {
        loginModal.style.display = "block";
    }

    // Open register modal
    registerBtn.onclick = () => {
        registerModal.style.display = "block";
    }

    // Close login modal
    loginClose.onclick = () => {
        loginModal.style.display = "none";
    }

    // Close register modal
    registerClose.onclick = () => {
        registerModal.style.display = "none";
    }

    // Close modals when clicking outside of them
    window.onclick = (event) => {
        if (event.target === loginModal) {
            loginModal.style.display = "none";
        }
        if (event.target === registerModal) {
            registerModal.style.display = "none";
        }
    }
});
