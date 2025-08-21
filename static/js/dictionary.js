document.addEventListener('DOMContentLoaded', () => {
  const table = document.querySelector('.dictionary-table');
  if (!table) return;

  const headers = table.querySelectorAll('th');

  headers.forEach((header, index) => {
    if (index === 0) return; // Skip Word No. column
    header.addEventListener('click', () => {
      const type = header.dataset.type || 'string';
      sortTableByColumn(table, index, type, header);
    });
  });
});

function sortTableByColumn(table, columnIndex, type, header) {
  const tbody = table.tBodies[0];
  const rows = Array.from(tbody.querySelectorAll('tr'));
  const isAscending = !header.classList.contains('sorted-asc');
  const dir = isAscending ? 1 : -1;

  rows.sort((a, b) => {
    const aText = a.children[columnIndex].textContent.trim();
    const bText = b.children[columnIndex].textContent.trim();
    let compare = 0;

    if (type === 'number') {
      compare = parseFloat(aText) - parseFloat(bText);
    } else if (type === 'date') {
      compare = new Date(aText) - new Date(bText);
    } else {
      compare = aText.localeCompare(bText);
    }
    return compare * dir;
  });

  table.querySelectorAll('th').forEach(th => th.classList.remove('sorted-asc', 'sorted-desc'));
  header.classList.toggle('sorted-asc', isAscending);
  header.classList.toggle('sorted-desc', !isAscending);

  rows.forEach(row => tbody.appendChild(row));
}
