"use strict";
(() => {
    const canvas = document.getElementById('route-canvas');
    if (!canvas) {
        console.error('Canvas element not found');
        return;
    }
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('Canvas 2D context not available');
        return;
    }
    const pointsList = document.getElementById('points-list');
    if (!pointsList) {
        console.error('Points list element not found');
        return;
    }
    const pointItems = pointsList.querySelectorAll('.point-item');
    const points = Array.from(pointItems).map(item => {
        const xAttr = item.getAttribute('data-x');
        const yAttr = item.getAttribute('data-y');
        return {
            x: xAttr ? parseFloat(xAttr) : 0,
            y: yAttr ? parseFloat(yAttr) : 0,
        };
    });
    let highlightedIndex = null;
    function redraw(ctx, canvas, points, highlightedIndex) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = 'red';
        ctx.fillStyle = 'blue';
        ctx.lineWidth = 2;
        if (points.length > 1) {
            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            for (let i = 1; i < points.length; i++) {
                ctx.lineTo(points[i].x, points[i].y);
            }
            ctx.stroke();
        }
        points.forEach((pt, i) => {
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, 4, 0, 2 * Math.PI);
            ctx.fill();
            if (i === highlightedIndex) {
                ctx.strokeStyle = 'orange';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, 8, 0, 2 * Math.PI);
                ctx.stroke();
                ctx.strokeStyle = 'red';
                ctx.lineWidth = 2;
            }
        });
    }
    redraw(ctx, canvas, points, highlightedIndex);
    pointItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            highlightedIndex = index;
            redraw(ctx, canvas, points, highlightedIndex);
        });
    });
})();
//# sourceMappingURL=highlightPoint.js.map