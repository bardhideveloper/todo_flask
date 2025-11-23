document.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flash-message");

    flashes.forEach(msg => {
        setTimeout(() => {
            msg.classList.add("fade-out");
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
});
