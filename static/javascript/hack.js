window.onload = function () {
  let star = document.getElementById("star");
  star.addEventListener("click", starTransform);

  let commentCheck = document.getElementById("checkComment");
  commentCheck.addEventListener("click", checkComment);
}

function starTransform() {
  star.style.backgroundColor="yellow";
  star.style.width="500px";
}

function checkComment() {
  let comment = document.getElementById("new_comment");
  entryValue = comment.value;

  if(entryValue.length>0) {
    let submit = document.getElementById("submitButton");
    submit.click();
  }
}
