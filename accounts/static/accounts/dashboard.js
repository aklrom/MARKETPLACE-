
document.addEventListener("DOMContentLoaded", () => {

    /*
     * =========================
     * REVEAL ANIMATION
     * =========================
     */

    const elements = document.querySelectorAll(".reveal");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.12
        }
    );

    elements.forEach((element) => {
        observer.observe(element);
    });


    /*
     * =========================
     * COUNTER ANIMATION
     * =========================
     */

    const counters = document.querySelectorAll("[data-counter]");

    counters.forEach((counter) => {
        const target = Number(counter.dataset.counter);

        if (Number.isNaN(target)) {
            return;
        }

        let current = 0;
        const duration = 900;
        const start = performance.now();

        function update(time) {
            const progress = Math.min(
                (time - start) / duration,
                1
            );

            const eased =
                1 - Math.pow(1 - progress, 3);

            current = Math.floor(target * eased);
            counter.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                counter.textContent = target;
            }
        }

        requestAnimationFrame(update);
    });


    /*
     * =========================
     * BUTTON FEEDBACK
     * =========================
     */

    const buttons = document.querySelectorAll(".btn");

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            button.classList.add("clicked");

            setTimeout(() => {
                button.classList.remove("clicked");
            }, 250);
        });
    });


    /*
     * =========================
     * CANCEL CONFIRMATION
     * =========================
     */

    const cancelForms = document.querySelectorAll(
        'form[action*="/cancel/"]'
    );

    cancelForms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            const confirmed = confirm(
                "Êtes-vous sûr de vouloir annuler cette commande ?"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

});

