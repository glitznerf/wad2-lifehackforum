window.onload = function () {
  let star = document.getElementById("star")
  star.onclick = function() {myFunction()};

  function myFunction() {
    star.style.backgroundColor="yellow";
    star.style.width="500px";
  }
}
