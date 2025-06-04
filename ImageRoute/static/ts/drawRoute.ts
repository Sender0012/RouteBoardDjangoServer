export type Point = { x: number; y: number };

export function drawRoute(
  points: Point[],
  imageId: string,
  canvasId: string,
  highlightPoint?: Point
): void {
  const canvas = document.getElementById(canvasId) as HTMLCanvasElement;
  const img = document.getElementById(imageId) as HTMLImageElement;
  const ctx = canvas.getContext("2d");

  function render() {
    if (!ctx || !canvas || !img) return;

    canvas.width = img.width;
    canvas.height = img.height;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "red";
    ctx.lineWidth = 2;
    ctx.beginPath();

    if (points.length > 0) {
      ctx.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
      }
      ctx.stroke();
    }

    for (const pt of points) {
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 4, 0, 2 * Math.PI);
      ctx.fillStyle = (highlightPoint && pt.x === highlightPoint.x && pt.y === highlightPoint.y)
        ? "orange"
        : "blue";
      ctx.fill();
    }
  }

  if (img.complete) {
    render();
  } else {
    img.onload = render;
  }
}

// Make it available globally for Django inline scripts
(window as any).drawRoute = drawRoute;
