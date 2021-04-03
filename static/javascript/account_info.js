window.onload = function () {
  let del = document.getElementById("delete_account_form")
  del.addEventListener("mouseover", confirmation());
  function confirmation() {
    return confirm('Do you really want to delete your account?');
  }
}
