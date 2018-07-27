// get all the h2 tags and the list
let h2 = document.getElementsByTagName("h2");
let indexUl = document.getElementById("indexList");
let h2Array = [];
pushArray(h2, h2Array);
createIndex(indexUl, h2Array);
let a = indexUl.querySelectorAll("a");
replaceAddHref(a);
replaceAddId(h2);

// function to push the h2 and h3 to a new array
function pushArray(array, newArray) {
  for (let item of array) {
    newArray.push(item);
  }
}

// insert the index
function createIndex(div, title){
  for(let item in title) {
    let index = `<li><a href="">${title[item].innerText}</a></li>`;
    div.insertAdjacentHTML("beforeend", index);
  }
}

// add the hrefs for the index
function replaceAddHref(array) {
  for (let item of array) {
    item.href = `#${replace(item)}`;
  }
}

// add the ids for the jumps
function replaceAddId(array) {
  for (let item of array) {
    item.id = replace(item);
  }
}

// function to replace spaces (" ") for "-"
function replace(item) {
  return item.innerText.replace(/\s/g, "-");
}