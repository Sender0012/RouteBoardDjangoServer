"use strict";
const rowsInput = document.getElementById('id_rows');
const colsInput = document.getElementById('id_cols');
const grid = document.getElementById('grid');
const colorPicker = document.getElementById('colorPicker');
const dotsDataInput = document.getElementById('id_dots_data');
let dots = [];
let activeColor = colorPicker.value;
function getDotCount(color) {
    return dots.filter(dot => dot.color === color).length;
}
function cellIsTaken(row, col) {
    return dots.some(dot => dot.row === row && dot.col === col);
}
function renderDot(cell, color) {
    const dot = document.createElement('div');
    dot.style.width = '20px';
    dot.style.height = '20px';
    dot.style.borderRadius = '50%';
    dot.style.backgroundColor = color;
    cell.appendChild(dot);
}
function generateGrid() {
    const rows = parseInt(rowsInput.value);
    const cols = parseInt(colsInput.value);
    if (isNaN(rows) || isNaN(cols) || rows <= 0 || cols <= 0) {
        alert("Podaj poprawne wymiary planszy.");
        return;
    }
    dots = [];
    dotsDataInput.value = '';
    grid.innerHTML = '';
    grid.style.display = 'grid';
    grid.style.gridTemplateColumns = `repeat(${cols}, 40px)`;
    grid.style.gap = '2px';
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = r.toString();
            cell.dataset.col = c.toString();
            cell.style.width = '40px';
            cell.style.height = '40px';
            cell.style.border = '1px solid #ccc';
            cell.style.display = 'flex';
            cell.style.justifyContent = 'center';
            cell.style.alignItems = 'center';
            cell.style.backgroundColor = 'white';
            cell.style.cursor = 'pointer';
            cell.addEventListener('click', () => {
                const row = parseInt(cell.dataset.row);
                const col = parseInt(cell.dataset.col);
                const color = activeColor;
                if (cellIsTaken(row, col))
                    return;
                if (getDotCount(color) >= 2)
                    return;
                dots.push({ row, col, color });
                renderDot(cell, color);
                dotsDataInput.value = JSON.stringify(dots);
            });
            grid.appendChild(cell);
        }
    }
}
colorPicker.addEventListener('input', e => {
    activeColor = e.target.value;
});
//# sourceMappingURL=board_editor.js.map