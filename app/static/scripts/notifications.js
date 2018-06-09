let notificacionModal = document.getElementById("notification");
let closeNotification = document.getElementById("close-notification");

function hideNotification() {
  notificacionModal.style.display = "none";
}

if (closeNotification) {
  closeNotification.addEventListener("click", hideNotification);
}