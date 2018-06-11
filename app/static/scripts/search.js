// get the elements of the search modal
let searchBar = document.getElementById("search-bar");
let searchIcon = document.getElementById("search-icon");
let searchMessage = document.getElementById("search-message");
let clearMessage = document.getElementById("clear-message");
let searchModal = document.getElementById("search-modal");
let results = document.getElementById("results");


// listen for clicks in the search icon and the gray background for the modal
searchIcon.addEventListener("click", showModal);
searchModal.addEventListener("click", removeBackground);

// listen for input in the searchBar
searchBar.addEventListener("keyup", filterTopics);

// local links for the index
let index = document.getElementById("index");
let a = index.querySelectorAll("a");
replaceAddHref(a);

// get h1, h2 (for the actual search)
let h2 = document.getElementsByTagName("h2");
let h3 = document.getElementsByTagName("h3");

// add the ids to h2s and h3s for the links jumps
replaceAddId(h2);
replaceAddId(h3);

// new list for h2 and h3 and the append functions
let topics = [];
pushArray(h2, topics);
pushArray(h3, topics);

// display all h2 and h3 en the results div and hide them
for (let item of topics) {
  let link = replace(item);
  results.insertAdjacentHTML(
    "beforeend",
    `<a style="display:none" href="#${link}" class="results_a">
        <p class="results_p">${item.innerText}</p>
      </a>`
  );
}

// get the anchors in the results div
let links = results.querySelectorAll("a");

// function to show the modal
function showModal() {
  searchModal.style.display = "block";
  searchBar.focus();
}

// the filter function
function filterTopics() {
  // get the values in the search bar
  let search = searchBar.value.toUpperCase();


  /* if there is text in the search bar, hide the default
  msg, show the clear link and the results div*/
  if (searchBar.value.length > 0) {
    searchMessage.style.display = "none";
    clearMessage.style.display = "block";
    results.style.display = "block";
  } else {
    // hide the clear msg and the results div, show the default msg
    clearMessage.style.display = "none";
    searchMessage.style.display = "block";
    results.style.display = "none";
  }

  // filter the topics using the search bar inputs
  for (let item of links) {
    if (item.innerText.toUpperCase().indexOf(search) > -1) {
      item.style.display = "block";
    } else {
      item.style.display = "none";
    }
  }
}

/* remove the gray background, except for the serachBar 
and the message area (clear the search bar) */
function removeBackground(e) {
  if (e.target == searchBar) {
    searchBar.focus();
  } else if (e.target == clearMessage) {
    // hide the clear message
    clearMessage.style.display = "none";
    // show the message
    searchMessage.style.display = "block";
    // delete the input in the search bar
    searchBar.value = "";
    // focus the page on the search bar
    searchBar.focus();

    for (let result of links) {
      result.style.display = "none";
    }

  } else {
    // hide the search modal
    searchModal.style.display = "none";
  }
}

// function to replace spaces (" ") for "-"
function replace(item) {
  return item.innerText.replace(/\s/g, "-");
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

// ctr+z to open the search modal and esc to close it
document.onkeyup = function (e) {
  if (e.ctrlKey && e.which == 90) {
    showModal();
  } else if (e.which == 27) {
    searchModal.style.display = "none";
  }
};