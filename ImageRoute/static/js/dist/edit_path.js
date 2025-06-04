// ─────────────────────────────────────────────────────────────────────────────
// edit_path.ts
// ─────────────────────────────────────────────────────────────────────────────
const gridContainer = document.getElementById("gridContainer");
const linesInput = document.getElementById("linesInput");
const form = document.getElementById("pathForm");
const colorSelector = document.getElementById("lineColorSelector");
let selectedStart = null;
let currentLineColor = "";
let dots = [...initialDots];
let lines = [...initialLines];
function dotKey(r, c) {
    return `${r}-${c}`;
}
function getDotAt(r, c) {
    return dots.find(d => d.row === r && d.col === c);
}
function cellOnLine(line, r, c) {
    const { from, to } = line;
    // Horizontal?
    if (from.row === to.row && r === from.row) {
        const minC = Math.min(from.col, to.col);
        const maxC = Math.max(from.col, to.col);
        return c >= minC && c <= maxC;
    }
    // Vertical?
    if (from.col === to.col && c === from.col) {
        const minR = Math.min(from.row, to.row);
        const maxR = Math.max(from.row, to.row);
        return r >= minR && r <= maxR;
    }
    return false;
}
// Check if the proposed line (from→to with color) is blocked by any dot/line of another color
function isBlocked(start, end, color) {
    // Only allow horizontal or vertical lines
    if (start.row !== end.row && start.col !== end.col) {
        return true;
    }
    const minR = Math.min(start.row, end.row);
    const maxR = Math.max(start.row, end.row);
    const minC = Math.min(start.col, end.col);
    const maxC = Math.max(start.col, end.col);
    // Iterate every cell strictly between start and end (inclusive)
    for (let r = minR; r <= maxR; r++) {
        for (let c = minC; c <= maxC; c++) {
            // Skip start & end
            if ((r === start.row && c === start.col) || (r === end.row && c === end.col)) {
                continue;
            }
            // 1) If a dot exists here of a different color → blocked
            const dot = getDotAt(r, c);
            if (dot && dot.color !== color) {
                return true;
            }
            // 2) If any existing line (of different color) occupies this cell → blocked
            const conflicting = lines.find(l => {
                if (l.from.color !== color) {
                    return cellOnLine(l, r, c);
                }
                return false;
            });
            if (conflicting) {
                return true;
            }
        }
    }
    // Check endpoints themselves: if endpoint has a dot of different color → blocked
    const dotAtStart = getDotAt(start.row, start.col);
    if (dotAtStart && dotAtStart.color !== color) {
        return true;
    }
    const dotAtEnd = getDotAt(end.row, end.col);
    if (dotAtEnd && dotAtEnd.color !== color) {
        return true;
    }
    // Check if endpoint lies on an existing line of different color → blocked
    const endpointConflict = lines.find(l => {
        if (l.from.color !== color) {
            return cellOnLine(l, end.row, end.col);
        }
        return false;
    });
    if (endpointConflict) {
        return true;
    }
    // All checks passed → not blocked
    return false;
}
function highlightCell(r, c, on) {
    const sel = `.grid-cell[data-row="${r}"][data-col="${c}"]`;
    const cell = document.querySelector(sel);
    if (cell) {
        cell.style.outline = on ? "2px solid red" : "none";
    }
}
function cancelSelection() {
    if (selectedStart) {
        highlightCell(selectedStart.row, selectedStart.col, false);
    }
    selectedStart = null;
}
// Paint the grid + dots, then overlay every line (including all cells on that line)
function drawGridAndLines() {
    gridContainer.innerHTML = "";
    gridContainer.style.display = "grid";
    gridContainer.style.gridTemplateColumns = `repeat(${boardCols}, 40px)`;
    gridContainer.style.gridTemplateRows = `repeat(${boardRows}, 40px)`;
    gridContainer.style.gap = "4px";
    // 1) Create every cell, and place dot if present
    for (let r = 0; r < boardRows; r++) {
        for (let c = 0; c < boardCols; c++) {
            const cell = document.createElement("div");
            cell.className = "grid-cell";
            cell.dataset.row = r.toString();
            cell.dataset.col = c.toString();
            const dot = getDotAt(r, c);
            if (dot) {
                const dotEl = document.createElement("div");
                dotEl.className = "dot";
                dotEl.style.backgroundColor = dot.color;
                cell.appendChild(dotEl);
            }
            // Clicking any cell attempts to start/finish a line
            cell.addEventListener("click", () => onCellClick(r, c));
            gridContainer.appendChild(cell);
        }
    }
    // 2) Draw every line—color all cells between endpoints inclusive
    lines.forEach((line) => {
        const { from, to } = line;
        const color = from.color;
        const minR = Math.min(from.row, to.row);
        const maxR = Math.max(from.row, to.row);
        const minC = Math.min(from.col, to.col);
        const maxC = Math.max(from.col, to.col);
        if (from.row === to.row) {
            // Horizontal: iterate columns
            for (let col = minC; col <= maxC; col++) {
                const sel = `.grid-cell[data-row="${from.row}"][data-col="${col}"]`;
                const cell = document.querySelector(sel);
                if (cell) {
                    cell.style.backgroundColor = color;
                }
            }
        }
        else {
            // Vertical: iterate rows
            for (let row = minR; row <= maxR; row++) {
                const sel = `.grid-cell[data-row="${row}"][data-col="${from.col}"]`;
                const cell = document.querySelector(sel);
                if (cell) {
                    cell.style.backgroundColor = color;
                }
            }
        }
    });
}
// Handles a click on cell (r,c)
function onCellClick(r, c) {
    if (selectedStart === null) {
        // First click: select start cell
        selectedStart = { row: r, col: c };
        highlightCell(r, c, true);
    }
    else {
        // Second click: validation + add line if valid
        const sx = selectedStart.row;
        const sy = selectedStart.col;
        const ex = r;
        const ey = c;
        const color = currentLineColor;
        // Attempt to draw from (sx,sy) → (ex,ey)
        if (isBlocked({ row: sx, col: sy }, { row: ex, col: ey }, color)) {
            alert("Nie można rysować przez inne kolory.");
            cancelSelection();
            return;
        }
        // Add the new line
        lines.push({
            from: { row: sx, col: sy, color },
            to: { row: ex, col: ey, color }
        });
        cancelSelection();
        drawGridAndLines();
    }
}
// Build <select> dropdown containing **only** dot‐colors
function populateColorSelector() {
    const usedColors = Array.from(new Set(dots.map(d => d.color)));
    usedColors.forEach((color) => {
        const opt = document.createElement("option");
        opt.value = color;
        opt.textContent = color;
        opt.style.backgroundColor = color;
        colorSelector.appendChild(opt);
    });
    currentLineColor = usedColors[0] || "#000000";
    colorSelector.value = currentLineColor;
    colorSelector.addEventListener("change", () => {
        currentLineColor = colorSelector.value;
    });
}
// Before the form submits, serialize `lines` into hidden input
form.addEventListener("submit", () => {
    linesInput.value = JSON.stringify(lines);
});
// INITIALIZE
populateColorSelector();
drawGridAndLines();
//export {};
//# sourceMappingURL=edit_path.js.map