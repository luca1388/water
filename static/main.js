document
  .getElementById("checkbox-zone-a")
  .addEventListener("click", function () {
    var checkboxA = document.getElementById("checkbox-zone-a");
    if (checkboxA.checked) {
      console.log("A: checked");
    } else {
      console.log("A: NOT checked");
    }
  });

  document
  .getElementById("checkbox-zone-b")
  .addEventListener("click", function () {
    var checkboxB = document.getElementById("checkbox-zone-b");
    if (checkboxB.checked) {
      console.log("B: checked");
    } else {
      console.log("B: NOT checked");
    }
  });
