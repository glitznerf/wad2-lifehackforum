
// Add event listeners at opening
window.onload = function () {
  let star = document.getElementById("star");
  star.addEventListener("click", starTransform);

  let commentCheck = document.getElementById("checkComment");
  commentCheck.addEventListener("click", checkComment);
}

// Resize star image
function starTransform() {
  star.style.backgroundColor="yellow";
  star.style.width="500px";
}

// Check that comment text is not empty
function checkComment() {
  let comment = document.getElementById("new_comment");
  entryValue = comment.value;

  if(entryValue.length>0) {
    let submit = document.getElementById("submitButton");
    submit.click();
  }
}
