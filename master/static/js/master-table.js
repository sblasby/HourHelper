document.addEventListener("DOMContentLoaded", function(){
    const employeeInput = document.getElementById("employee-field");
    const employeeDrop = document.getElementById("employee-drop");

    employeeInput.addEventListener("focus", function(){
        employeeDrop.style.display = "block";
    });

    // Use mousedown instead of click for better interaction with the dropdown
    employeeDrop.addEventListener("mousedown", function(event){
        const target = event.target;
        
        if (target.classList.contains("employee-select")) {
            let value = target.textContent;
            employeeInput.value = value;
            employeeDrop.style.display = "none";
        }
    });

    // Use mouseup to prevent the blur event from hiding the dropdown when clicking on items
    employeeInput.addEventListener("mouseup", function(event){
        event.stopPropagation();
    });

    document.addEventListener("mouseup", function(){
        employeeDrop.style.display = "none";
    });
});

