// get the scroll btn
let scrollButton = document.getElementById('scroll'); // Reference to our scroll button

// hide scroll button
scrollButton.style.display = 'none';

window.onscroll = function () {
  scrollFunction();
};

// When the user scrolls down 200px from the top of the document, show the button
function scrollFunction() {
  if (document.documentElement.scrollTop > 200) {
    scrollButton.style.display = 'block';
  } else {
    scrollButton.style.display = 'none';
  }
}

/** Scroll to top button implementation in vanilla JavaScript (ES6 - ECMAScript 6) **/
let intervalId = 0; // Needed to cancel the scrolling when we're at the top of the page

function scrollStep() {
  // Check if we're at the top already. If so, stop scrolling by clearing the interval
  if (window.pageYOffset === 0) {
    clearInterval(intervalId);
  }
  window.scroll(0, window.pageYOffset - 2000);
}

function scrollToTop() {
  // Call the function scrollStep() every 16.66 millisecons
  intervalId = setInterval(scrollStep, 16.66);
}

// When the DOM is loaded, this click handler is added to our scroll button
scrollButton.addEventListener('click', scrollToTop);