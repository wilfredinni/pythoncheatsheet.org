// get deleteModal, deleteModalBtn and closeBrn by id
let deleteModal = document.getElementById('deleteModal');
let deleteModalBtns = document.getElementsByClassName('deleteModalBtn');
let closeBtn = document.getElementById('closeBtn');
let cancel = document.getElementById('cancel');

// arrows functions to open and close the modals
const openModal = () => deleteModal.classList.add('is-active');
const closeModal = () => deleteModal.classList.remove('is-active');

// listen every delete button from overview and manage articles
for (let button of deleteModalBtns) {
    button.addEventListener('click', openModal);
}

// listen for clicks to close the modal
closeBtn.addEventListener('click', closeModal);
modalBackground.addEventListener('click', closeModal);
cancel.addEventListener('click', closeModal);

// ----------------------------------------------------------------------------