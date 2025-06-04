document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("gameboard-form") as HTMLFormElement;
  const gridContainer = document.getElementById("grid")!;
  const colorPicker = document.getElementById("colorPicker") as HTMLInputElement;
  const generateButton = document.getElementById("generateGridButton") as HTMLButtonElement;
  const dotsDataField = document.querySelector("input[name='dots_data']") as HTMLInputElement;
  const rowsInput = document.querySelector("input[name='rows']") as HTMLInputElement;
  const colsInput = document.querySelector("input[name='cols']") as HTMLInputElement;

  let selectedDots: { row: number; col: number; color: string }[] = [];

  generateButton.addEventListener("click", () => {
    const rows = parseInt(rowsInput.value);
    const cols = parseInt(colsInput.value);
    if (isNaN(rows) || isNaN(cols) || rows <= 0 || cols <= 0) return;

    gridContainer.innerHTML = "";
    selectedDots = [];

    const grid = document.createElement("div");
    grid.className = "grid";
    grid.style.display = "grid";
    grid.style.gridTemplateRows = `repeat(${rows}, 30px)`;
    grid.style.gridTemplateColumns = `repeat(${cols}, 30px)`;
    grid.style.gap = "5px";

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const cell = document.createElement("div");
        cell.className = "grid-cell";
        cell.style.width = "30px";
        cell.style.height = "30px";
        cell.style.border = "1px solid #ccc";
        cell.style.borderRadius = "5px";
        cell.style.backgroundColor = "#fff";
        cell.style.cursor = "pointer";
        cell.style.transition = "background-color 0.3s";

        cell.dataset.row = r.toString();
        cell.dataset.col = c.toString();

        cell.addEventListener("click", () => {
          const color = colorPicker.value;
          cell.style.backgroundColor = color;

          selectedDots = selectedDots.filter(dot => !(dot.row === r && dot.col === c));
          selectedDots.push({ row: r, col: c, color });
        });

        grid.appendChild(cell);
      }
    }

    gridContainer.appendChild(grid);
  });

  form.addEventListener("submit", () => {
    dotsDataField.value = JSON.stringify(selectedDots);
  });
});