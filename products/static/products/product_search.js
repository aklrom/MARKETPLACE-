/* ============================================================
   product_search.js : recherche instantanée dans la liste des produits
   - filtre pendant la frappe, sans recharger la page
   - ignore les accents et les majuscules ("velo" trouve "Vélo")
   - plusieurs mots : tous doivent être présents ("samsung 128")
   - cherche dans le nom, la catégorie et l'état du produit
   ============================================================ */
(function () {
    "use strict";

    var form = document.getElementById("product-search-form");
    var input = document.getElementById("product-search");
    var items = document.querySelectorAll("[data-search]");

    // Pas de produits : la barre reste cachée
    if (!form || !input || !items.length) {
        return;
    }

    var count = document.getElementById("result-count");
    var empty = document.getElementById("no-results");
    var emptyTerm = document.getElementById("no-results-term");
    var clearInside = document.getElementById("search-clear");
    var clearButtons = document.querySelectorAll("[data-search-clear]");
    var total = items.length;

    function normalize(text) {
        return text
            .toLowerCase()
            .normalize("NFD")
            .replace(/[̀-ͯ]/g, "")
            .replace(/\s+/g, " ")
            .trim();
    }

    function plural(n) {
        return n > 1 ? "s" : "";
    }

    // Texte de chaque produit, préparé une seule fois
    var index = Array.prototype.map.call(items, function (element) {
        return { element: element, text: normalize(element.getAttribute("data-search")) };
    });

    function apply() {
        var query = normalize(input.value);
        var words = query ? query.split(" ") : [];
        var visible = 0;

        index.forEach(function (entry) {
            var match = words.every(function (word) {
                return entry.text.indexOf(word) !== -1;
            });
            entry.element.hidden = !match;
            if (match) {
                visible += 1;
            }
        });

        if (count) {
            count.textContent = words.length
                ? visible + " résultat" + plural(visible) + " sur " + total
                : total + " annonce" + plural(total);
        }
        if (empty) {
            empty.hidden = visible > 0;
            if (emptyTerm) {
                emptyTerm.textContent = "« " + input.value.trim() + " »";
            }
        }
        if (clearInside) {
            clearInside.hidden = input.value === "";
        }
    }

    function clear() {
        input.value = "";
        apply();
        input.focus();
    }

    form.hidden = false; // la barre n'apparaît que si le JavaScript fonctionne

    input.addEventListener("input", apply);

    input.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && input.value) {
            event.preventDefault();
            clear();
        }
    });

    // Entrée ou « Rechercher » du clavier mobile : on ferme le clavier, sans recharger
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        input.blur();
    });

    clearButtons.forEach(function (button) {
        button.addEventListener("click", clear);
    });

    apply(); // le navigateur peut avoir rempli le champ (retour arrière)
})();
