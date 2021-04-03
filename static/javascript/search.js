window.onload = function () {
  let search = document.getElementById("searchBar");
  search.addEventListener("keyup", searchFct);
}


function searchFct() {
  // Variable declaration
  var search, filter, list, entries, entry, i, entryValue;

  // DOM setup
  search = document.getElementById("searchBar");
  list = document.getElementById("list");
  entries = list.getElementsByTagName('a');

  // Get filter text
  filter = search.value.toUpperCase();

  // Hide entries in list that don't match search query
  for (i = 0; i < entries.length; i++) {
    entry = entries[i].getElementsByTagName("h2")[0];
    entryValue = entry.textContent || entry.innerText;
    if (entryValue.toUpperCase().indexOf(filter) > -1) {
      entries[i].style.display = "";
    } else {
      entries[i].style.display = "none";
    }
  }
}
