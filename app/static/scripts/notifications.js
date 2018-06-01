let notificacionModal = document.getElementById("notification");
let closeNotification = document.getElementById("close-notification");

function hideNotification() {
    notificacionModal.style.display = "none";
}

closeNotification.addEventListener("click", hideNotification);