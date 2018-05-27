// get the search bar and the gray background
let searchBar = document.getElementById('search-bar');
let searchBackground = document.getElementById('search-modal');

// get h1 and h2 tags
let h2 = document.getElementsByTagName('h2');
let h3 = document.getElementsByTagName('h3');


function listH2H3() {

    // show the gray transparent background
    searchBackground.style.display = 'block';

    for (let item of h2) {
        console.log('h2: ' + item.innerHTML);
    }

    for (let item of h3) {
        console.log('h3: ' + item.innerHTML);
    }
}

// function to remove the gray background
function removeBackground() {
    searchBackground.style.display = 'none';
}

// listen for clicks in the search bar and the gray background
searchBar.addEventListener('click', listH2H3);
searchBackground.addEventListener('click', removeBackground);