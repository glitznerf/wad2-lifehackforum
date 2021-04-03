window.onload = function () {
  let delCheck = document.getElementById("checkDeleteButton");
  delCheck.addEventListener("click", confirmation);
}

function confirmation() {
  if(confirm('Do you really want to delete your account?')) {
    let del = document.getElementById("submitButton");
    del.click();
  }
}
