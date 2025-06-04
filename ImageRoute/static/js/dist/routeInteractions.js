import { drawRoute } from "./drawRoute";
window.addEventListener("DOMContentLoaded", () => {
    const image = document.getElementById("background-image");
    const canvasId = "route-canvas";
    const inputX = document.getElementById("input-x");
    const inputY = document.getElementById("input-y");
    // Click on image populates form
    image.addEventListener("click", (e) => {
        const rect = image.getBoundingClientRect();
        const x = Math.round(e.clientX - rect.left);
        const y = Math.round(e.clientY - rect.top);
        inputX.value = x.toString();
        inputY.value = y.toString();
    });
    // Highlight points on hover
    const listItems = document.querySelectorAll("li[data-x][data-y]");
    listItems.forEach((li) => {
        li.addEventListener("mouseenter", () => {
            const x = parseInt(li.getAttribute("data-x") || "0", 10);
            const y = parseInt(li.getAttribute("data-y") || "0", 10);
            drawRoute(window.points, "background-image", canvasId, { x, y });
        });
        li.addEventListener("mouseleave", () => {
            drawRoute(window.points, "background-image", canvasId);
        });
    });
});
//# sourceMappingURL=routeInteractions.js.map