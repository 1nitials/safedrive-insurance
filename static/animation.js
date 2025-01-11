document.addEventListener("DOMContentLoaded", () => {
    const content = document.querySelector(".container");
    if (content) {
        content.classList.add("fade-in");
    }

    // Intercept navigation links for smooth transitions
    const links = document.querySelectorAll(".nav-buttons a, .back-button a");
    links.forEach(link => {
        link.addEventListener("click", event => {
            event.preventDefault(); // Stop the default navigation

            const href = link.getAttribute("href");
            if (content) {
                content.classList.add("fade-out"); // Apply fade-out animation
                setTimeout(() => {
                    window.location.href = href; // Navigate after animation
                }, 300); // Match this duration to the fade-out transition
            }
        });
    });
});
