const gridContainer = document.getElementById("gridContainer");
const generateGridButton = document.getElementById("generateGrid");
const saveBoardButton = document.getElementById("saveBoard");
const colorPicker = document.getElementById("colorPicker");
const dotsInput = document.querySelector("input[name='dots']");
let currDots = [];
let rows = 0;
let cols = 0;
function countColor(color) {
    return currDots.filter(dot => dot.color === color).length;
}
function generateGrid() {
    currDots = [];
    gridContainer.innerHTML = "";
    const rowsInput = document.querySelector("input[name='rows']");
    const colsInput = document.querySelector("input[name='cols']");
    rows = parseInt(rowsInput.value);
    cols = parseInt(colsInput.value);
    if (!rowsInput || !colsInput) {
        console.error("Missing rows or cols input fields");
        return;
    }
    gridContainer.style.display = "grid";
    gridContainer.style.gridTemplateRows = `repeat(${rows}, 40px)`;
    gridContainer.style.gridTemplateColumns = `repeat(${cols}, 40px)`;
    gridContainer.style.gap = "4px";
    console.log("Console is working ✅");
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const cell = document.createElement("div");
            cell.classList.add("grid-cell");
            cell.dataset.row = r.toString();
            cell.dataset.col = c.toString();
            cell.addEventListener("click", () => {
                const color = colorPicker.value;
                const row = parseInt(cell.dataset.row);
                const col = parseInt(cell.dataset.col);
                const alreadyPlaced = currDots.find(dot => dot.row === row && dot.col === col);
                if (alreadyPlaced) {
                    alert("there is a dot here");
                    return; // prevent overwriting
                }
                if (countColor(color) >= 2) {
                    alert("Only two dots allowed per color.");
                    return;
                }
                const dot = document.createElement("div");
                dot.classList.add("dot");
                dot.style.backgroundColor = color;
                cell.appendChild(dot);
                //                 cell.style.backgroundColor = color;
                currDots.push({ row, col, color });
            });
            gridContainer.appendChild(cell);
        }
    }
}
generateGridButton.addEventListener("click", generateGrid);
function saveBoard() {
    dotsInput.value = JSON.stringify(currDots);
    document.getElementById("boardForm").submit();
}
saveBoardButton.addEventListener("click", saveBoard);
if (typeof initialDots !== "undefined") {
    currDots = initialDots;
    window.addEventListener("load", () => {
        const rowsInput = document.querySelector("input[name='rows']");
        const colsInput = document.querySelector("input[name='cols']");
        if (rowsInput.value && colsInput.value)
            generateGrid();
        for (const dot of initialDots) {
            const cell = document.querySelector(`td[data-row="${dot.row}"][data-col="${dot.col}"]`);
            if (cell) {
                cell.style.backgroundColor = dot.color;
            }
        }
    });
}
//export {};
//# sourceMappingURL=new_gameboard.js.map