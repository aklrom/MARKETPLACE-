/* ============================================================
   product_form.js : aperçu de la photo choisie + contrôle du fichier
   (confort pour l'utilisateur ; le serveur doit aussi vérifier)
   ============================================================ */
(function () {
    "use strict";

    var MAX_MB = 5;
    var input = document.getElementById("id_image");
    if (!input) {
        return;
    }

    var preview = document.createElement("img");
    preview.className = "image-preview";
    preview.alt = "Aperçu de la photo";
    preview.hidden = true;

    var error = document.createElement("div");
    error.className = "text-danger small mt-1";
    error.hidden = true;

    // Ordre final : champ fichier, message d'erreur, aperçu
    input.after(preview);
    input.after(error);

    var currentUrl = null;

    function reset() {
        if (currentUrl) {
            URL.revokeObjectURL(currentUrl);
            currentUrl = null;
        }
        preview.hidden = true;
        preview.removeAttribute("src");
        error.hidden = true;
        error.textContent = "";
    }

    function reject(message) {
        error.textContent = message;
        error.hidden = false;
        input.value = "";
    }

    input.addEventListener("change", function () {
        reset();

        var file = input.files && input.files[0];
        if (!file) {
            return;
        }
        if (file.type.indexOf("image/") !== 0) {
            reject("Ce fichier n'est pas une image.");
            return;
        }
        if (file.size > MAX_MB * 1024 * 1024) {
            reject("L'image est trop lourde (maximum " + MAX_MB + " Mo).");
            return;
        }

        currentUrl = URL.createObjectURL(file);
        preview.src = currentUrl;
        preview.hidden = false;
    });
})();