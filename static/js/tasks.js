document.addEventListener("DOMContentLoaded", () => {

    // Sortable list handling
    const list = document.getElementById("tasks-list");

    if (list) {
        Sortable.create(list, {
            animation: 150,
            onEnd: () => {
                const order = Array.from(list.children).map((li, i) => ({
                    id: li.dataset.id,
                    order: i
                }));
                fetch("/reorder", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(order),
                });
            }
        });
    }

    // Modal handling
    const modal = document.getElementById("editModal");
    const modalBody = document.getElementById("modal-body");
    const closeModal = document.getElementById("closeModal");

    document.querySelectorAll(".edit-btn").forEach(btn => {
        btn.addEventListener("click", async (e) => {
            e.preventDefault();

            const url = btn.getAttribute("href");
            const res = await fetch(url);
            const html = await res.text();

            modalBody.innerHTML = html;
            modal.style.display = "flex";

            const form = document.getElementById("edit-task-form");
            form.addEventListener("submit", async (evt) => {
                evt.preventDefault();

                const formData = new FormData(form);
                const response = await fetch(form.action, {
                    method: "POST",
                    body: formData
                });

                if (response.redirected) {
                    window.location = response.url;
                    return;
                }

                const json = await response.json();

                if (json.success) {
                    location.reload();
                }
            });
        });
    });

    if (closeModal) {
        closeModal.onclick = () => (modal.style.display = "none");
        window.onclick = (e) => {
            if (e.target === modal) modal.style.display = "none";
        };
    }
});
