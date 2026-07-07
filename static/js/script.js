// Student ID: 25060488
// Name: Renat Bershadskyi
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

async function editField(field, displayId) {
    let currentValue = document.getElementById(displayId).textContent;

    if (currentValue === "Not set") currentValue = "";

    let newValue;

    if (field === "user_dob") {
        newValue = prompt("Enter date of birth (YYYY-MM-DD):", currentValue);
    } else {
        newValue = prompt("Enter new value:", currentValue);
    }

    if (!newValue || newValue === currentValue) return;

    // DOB validation
    if (field === "user_dob") {
        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;

        if (!dateRegex.test(newValue)) {
            alert("Invalid DOB format. Use YYYY-MM-DD");
            return;
        }

        const date = new Date(newValue);
        if (date > new Date()) {
            alert("DOB cannot be in the future");
            return;
        }
    }

    const res = await fetch("/update_profile", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            field: field,
            value: newValue
        })
    });

    const data = await res.json();

    if (data.success) {
        document.getElementById(displayId).textContent = newValue;
    } else {
        alert("Update failed");
    }
}