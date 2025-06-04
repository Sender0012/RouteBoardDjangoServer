
// addPointClick.ts
window.addEventListener("DOMContentLoaded", () => {
    const img = document.getElementById("background-image");
    const canvas = document.getElementById("click-canvas");
    const ctx = canvas.getContext("2d");
    //   // Adjust canvas size to match image once loaded
    //   img.onload = () => {
    //     canvas.width = img.width;
    //     canvas.height = img.height;
    //   };
    //   if (img.complete) {
    //     // In case image already loaded
    //     canvas.width = img.width;
    //     canvas.height = img.height;
    //   }
    canvas.width = img.width;
    canvas.height = img.height;
    // Get form inputs for x and y
    const inputX = document.querySelector("input[name='x']");
    const inputY = document.querySelector("input[name='y']");
    img.addEventListener("click", (e) => {
        if (!ctx)
            return;
        // Calculate click position relative to image
        const rect = img.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        // Set form values
        inputX.value = Math.round(x).toString();
        inputY.value = Math.round(y).toString();
        // Clear canvas and draw circle where clicked
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, 2 * Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();
    });
});
//# sourceMappingURL=addPointClick.js.map