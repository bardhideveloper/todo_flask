function filterTable(tableId, searchValue) {
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
    const filter = searchValue.toLowerCase();

    for (let i = 0; i < rows.length; i++) {
        let textContent = rows[i].textContent.toLowerCase();
        rows[i].style.display = textContent.includes(filter) ? "" : "none";
    }
}