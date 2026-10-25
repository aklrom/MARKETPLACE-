/* ============================================================
   site.js : comportements communs (pages qui héritent de base.html)
   1. Confirmation avant une action sensible : <form data-confirm="...">
   2. Anti double-clic : un formulaire ne part qu'une seule fois
   3. Les messages de succès disparaissent seuls
   ============================================================ */
(function () {
    "use strict";

    // 1 + 2. Gestion de l'envoi des formulaires
    document.addEventListener("submit", function (event) {
        var form = event.target;

        if (event.defaultPrevented || !(form instanceof HTMLFormElement)) {
            return;
        }

        var message = form.getAttribute("data-confirm");
        if (message && !window.confirm(message)) {
            event.preventDefault();
            return;
        }

        if (form.dataset.submitting === "1") {
            event.preventDefault();
            return;
        }
        form.dataset.submitting = "1";

        form.querySelectorAll("button:not([type]), button[type='submit']").forEach(function (button) {
            button.dataset.label = button.textContent;
            button.textContent = "Patientez…";
            button.setAttribute("aria-busy", "true");
            button.disabled = true;
        });
    });

    // Retour arrière du navigateur : on réactive les boutons
    window.addEventListener("pageshow", function (event) {
        if (!event.persisted) {
            return;
        }
        document.querySelectorAll("form[data-submitting]").forEach(function (form) {
            delete form.dataset.submitting;
            form.querySelectorAll("button[aria-busy]").forEach(function (button) {
                button.textContent = button.dataset.label || button.textContent;
                button.removeAttribute("aria-busy");
                button.disabled = false;
            });
        });
    });

    // 3. Messages : disparition au bout de 5 secondes
    function hideMessages() {
        document.querySelectorAll(".alert[data-autohide]").forEach(function (alertBox) {
            window.setTimeout(function () {
                alertBox.classList.add("is-hiding");
                window.setTimeout(function () {
                    alertBox.remove();
                }, 500);
            }, 5000);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", hideMessages);
    } else {
        hideMessages();
    }
})();