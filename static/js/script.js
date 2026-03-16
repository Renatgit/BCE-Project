function matchBlockHeights() {
    document.querySelectorAll(".matchHeights").forEach(section => {
        const image = section.querySelector(".bg-img");
        if (image) {
            section.style.height = image.clientHeight + "px";
        }
    });
}

function closePanels() {
    document.querySelectorAll(".filters-panel, .sort-panel").forEach(panel => {
        panel.classList.add("d-none");
    });
}

function openPanel(panelId) {
    closePanels();
    const panel = document.getElementById(panelId);
    if (panel) {
        panel.classList.remove("d-none");
    }
}

function initFilterSortPanels() {
    const filterBtn = document.getElementById("openFiltersBtn");
    const sortBtn = document.getElementById("openSortBtn");

    filterBtn?.addEventListener("click", (event) => {
        event.stopPropagation();
        openPanel("filtersPanel");
    });

    sortBtn?.addEventListener("click", (event) => {
        event.stopPropagation();
        openPanel("sortPanel");
    });

    document.addEventListener("click", (event) => {
        const clickedInsidePanel = Boolean(
            event.target.closest(".filters-panel") || event.target.closest(".sort-panel")
        );
        const clickedPanelButton = Boolean(
            event.target.closest("#openFiltersBtn") || event.target.closest("#openSortBtn")
        );

        if (!clickedInsidePanel && !clickedPanelButton) {
            closePanels();
        }
    });
}

function init() {
    matchBlockHeights();
    initFilterSortPanels();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
} else {
    init();
}

window.addEventListener("resize", matchBlockHeights);
