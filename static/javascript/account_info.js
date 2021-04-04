
// Add event listeners at opening
window.onload = function () {
  let delCheck = document.getElementById("checkDeleteButton");
  delCheck.addEventListener("click", confirmation);
}

// Have a simple confirmation popup window before deleting the account
function confirmation() {
  if(confirm('Do you really want to delete your account?')) {
    let del = document.getElementById("submitButton");
    del.click();
  }
}
