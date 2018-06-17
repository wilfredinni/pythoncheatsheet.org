// dashboard main section: pin message
let pinMsgTitle = document.getElementById("pinMsgTitle");
let pinMsgContent = document.getElementById("pinMsgContent");

// functions to show and hide sections on the site configuration
function showHidePinMsg() {
  if (pinMsgContent.style.display == "block") {
    pinMsgContent.style.display = "none";
  } else {
    pinMsgContent.style.display = "block";
  }
}

// listen for clicks in the pinned msg title
if (pinMsgTitle) {
  pinMsgTitle.addEventListener("click", showHidePinMsg);
}