document
  .getElementById("checkbox-zone-a")
  .addEventListener("click", function () {
    var checkboxA = document.getElementById("checkbox-zone-a");
    var state = 'off';
    if (checkboxA.checked) {
      console.log("A: checked");
      state = 'on';
      
    } else {
      console.log("A: NOT checked");
      state = 'off';
    }
    fetch("/valves/a", {
        method: "PUT",
        body: JSON.stringify({ data: { state: state } }),
      })
        .then((response) => response.json())
        .then((result) => console.log(result))
        .catch((e) => console.log(e));
  });

document
  .getElementById("checkbox-zone-b")
  .addEventListener("click", function () {
    var checkboxB = document.getElementById("checkbox-zone-b");
    var state = 'off';
    if (checkboxB.checked) {
      console.log("B: checked");
      state = 'on';
    } else {
      console.log("B: NOT checked");
      state = 'off';
    }
    fetch("/valves/a", {
        method: "PUT",
        body: JSON.stringify({ data: { state: state } }),
      })
        .then((response) => response.json())
        .then((result) => console.log(result))
        .catch((e) => console.log(e));
  });
