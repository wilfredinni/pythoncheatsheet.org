// get deleteModal, deleteModalBtn and closeBrn by id
let deleteModal = document.getElementById("deleteModal");
let deleteModalBtns = document.getElementsByClassName("deleteModalBtn");
let closeBtn = document.getElementById("closeBtn");
let cancel = document.getElementById("cancel");
let closeNotificationButton = document.getElementById("close-notification");
let notification = document.getElementById("close-notification");

// arrows functions to open and close the modals
const openModal = () => deleteModal.classList.add("is-active");
const closeModal = () => deleteModal.classList.remove("is-active");
const closeNoti = () => notification.style.display = "none";

// listen every delete button from overview and manage articles
for (let button of deleteModalBtns) {
  button.addEventListener("click", openModal);
}

closeNotificationButton.addEventListener("click", closeNoti);

// listen for clicks to close the modal
if (closeBtn) {
  closeBtn.addEventListener("click", closeModal);
  cancel.addEventListener("click", closeModal);
}

// ----------------------------------------------------------------------------