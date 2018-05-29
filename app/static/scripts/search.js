// get the search bar and the gray background for the modal
let searchBar = document.getElementById('search-bar');
let searchIcon = document.getElementById('search-icon');
let searchBackground = document.getElementById('search-modal');

// listen for clicks in the search bar and the gray background for the modal
searchIcon.addEventListener('click', showModal);
searchBackground.addEventListener('click', removeBackground);

// get h1, h2 and te results div (for the actual search)
let h2 = document.getElementsByTagName('h2');
let h3 = document.getElementsByTagName('h3');

// local links for the index
let index = document.getElementById('index');
let a = index.querySelectorAll('a');
replaceAddHref(a);

// add the ids to h2s and h3s for the links jumps
replaceAddId(h2);
replaceAddId(h3);


// new list for h2 and h3
let topics = [];
// append h2 and h3
pushArray(h2, topics);
pushArray(h3, topics);

// listen for input in the searchBar
searchBar.addEventListener('keyup', filterTopics);

// display all h2 and h3 en the results div and hide them
let results = document.getElementById('results');
for (let item of topics) {
  let link = replace(item);
  results.insertAdjacentHTML('beforeend', `<a style="display:none" href="#${link}" class="results_a">
        <p class="results_p">${item.innerText}</p>
      </a>`);
}

// the filter function
function filterTopics() {
  // get the value of an input
  let search = searchBar.value.toUpperCase();
  // get the results div
  let links = results.querySelectorAll('a');

  for (let item of links) {
    if (item.innerText.toLocaleUpperCase().indexOf(search) > 0) {
      item.style.display = 'block';
    } else {
      item.style.display = 'none';
    }
  }
}

// function to show the modal 
function showModal() {
  searchBackground.style.display = 'block';
}

// remove the gray background, except for the serachBar
function removeBackground(e) {
  if (e.target != searchBar) {
    searchBackground.style.display = 'none';
  }
}

// function to replace spaces for '-'
function replace(item) {
  return item.innerText.replace(/\s/g, '-');
}

// function to push the h2 and h3 to a new array
function pushArray(array, newArray) {
  for (let item of array) {
    newArray.push(item);
  }
}

// add the ids for the jumps
function replaceAddId(array) {
  for (let item of array) {
    item.id = replace(item);
  }
}

// add the hrefs for the index
function replaceAddHref(array) {
  for (let item of array) {
    item.href = `#${replace(item)}`;
  }
}