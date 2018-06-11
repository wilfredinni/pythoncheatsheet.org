//navbar burger
(function () {
  var burger = document.querySelector(".burger");
  var nav = document.querySelector("#" + burger.dataset.target);

  burger.addEventListener("click", function () {
    burger.classList.toggle("is-active");
    nav.classList.toggle("is-active");
  });
})();


// get deleteModal, deleteModalBtn and closeBtn for articles page
let deleteModal = document.getElementById("deleteModal");
let deleteArticleBtn = document.getElementById("deleteArticleBtn");
let closeBtn = document.getElementById("closeBtn");
let cancel = document.getElementById("cancel");
let articleModalBackground = document.getElementById("articleModalBackground");
let articleEdits = document.getElementById("articleEdits");

// pysheet notification
let notification = document.getElementById("pysheetNotification");
let closeNotificationButton = document.getElementById("pysheetCloseNotification");

// main notifications
let mainNotification = document.getElementById("mainNotification");
let closeMainNotification = document.getElementById("closeMainNotification");

// arrows functions to open and close the modals
const openModal = () => deleteModal.classList.add("is-active");
const closeModal = () => deleteModal.classList.remove("is-active");
const closePysheetNoti = () => notification.style.display = "none";
const closeMainNoti = () => mainNotification.style.display = "none";

// listen for close button in the pysheet
if (closeNotificationButton) {
  closeNotificationButton.addEventListener("click", closePysheetNoti);
}

// listen for main notifications
if (mainNotification) {
  closeMainNotification.addEventListener("click", closeMainNoti);
}

// listen for clicks to close the modal
if (articleEdits) {
  deleteArticleBtn.addEventListener("click", openModal);
  closeBtn.addEventListener("click", closeModal);
  cancel.addEventListener("click", closeModal);
  articleModalBackground.addEventListener("click", closeModal);
}