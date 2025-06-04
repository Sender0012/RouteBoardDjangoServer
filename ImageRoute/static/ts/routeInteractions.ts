import { drawRoute, Point } from "./drawRoute";

declare global {
  interface Window {
    drawRoute: typeof drawRoute;
    points: Point[];
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const image = document.getElementById("background-image") as HTMLImageElement;
  const canvasId = "route-canvas";

  const inputX = document.getElementById("input-x") as HTMLInputElement;
  const inputY = document.getElementById("input-y") as HTMLInputElement;

  // Click on image populates form
  image.addEventListener("click", (e: MouseEvent) => {
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
