// dashboard main section: pin message
let pinMsgTitle = document.getElementById("pinMsgTitle");
let pinMsgContent = document.getElementById("pinMsgContent");

// new post main sections
let h1Title = document.getElementById("h1Title");
let titleSumImg = document.getElementById("titleSumImg");
let h1Body = document.getElementById("h1Body");
let articleBody = document.getElementById("articleBody");
let h1Tags = document.getElementById("h1Tags");
let tagArtUrl = document.getElementById("tagArtUrl");

// function to show and hide new post divs
function showHideTitle() {
  if (titleSumImg.style.display == "block") {
    titleSumImg.style.display = "none";
  } else {
    titleSumImg.style.display = "block";
  }
}

function showHideBody() {
  if (articleBody.style.display == "block") {
    articleBody.style.display = "none";
  } else {
    articleBody.style.display = "block";
  }
}

function showHideTags() {
  if (tagArtUrl.style.display == "block") {
    tagArtUrl.style.display = "none";
  } else {
    tagArtUrl.style.display = "block";
  }
}

// functions to show and hide sections on the site configuration
function showHidePinMsg() {
  if (pinMsgContent.style.display == "block") {
    pinMsgContent.style.display = "none";
  } else {
    pinMsgContent.style.display = "block";
  }
}

// list for click in new post
if (h1Title) {
  h1Title.addEventListener("click", showHideTitle);
}

if (h1Body) {
  h1Body.addEventListener("click", showHideBody);
}

if (h1Tags) {
  h1Tags.addEventListener("click", showHideTags);
}

// listen for clicks in the pinned msg title
if (pinMsgTitle) {
  pinMsgTitle.addEventListener("click", showHidePinMsg);
}