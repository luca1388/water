document.addEventListener(
  document.getElementById("checkbox-zone-a"),
  "click",
  function () {
      var checkboxA = document.getElementById("checkbox-zone-a");
      if (checkboxA.checked) {
        console.log('A: checked');
      } else {
        console.log('A: NOT checked');
      }
  }
);
