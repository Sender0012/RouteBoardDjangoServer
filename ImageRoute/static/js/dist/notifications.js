"use strict";
// static/js/notifications.ts
const eventSource = new EventSource('/sse/notifications/');
eventSource.addEventListener("newBoard", (event) => {
    const data = JSON.parse(event.data);
    showToast(`Użytkownik ${data.creator_username} utworzył nową planszę: ${data.board_name}`);
});
eventSource.addEventListener("newPath", (event) => {
    const data = JSON.parse(event.data);
    showToast(`Użytkownik ${data.user_username} zapisał ścieżkę na planszy: ${data.board_name}`);
});
eventSource.onerror = () => {
    console.error("Błąd połączenia SSE");
};
function showToast(message) {
    const toast = document.createElement('div');
    toast.innerText = message;
    toast.className = 'toast';
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 5000);
}
//# sourceMappingURL=notifications.js.map