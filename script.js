let bids = [];

function renderTable() {
  const tbody = document.getElementById('bidsBody');
  tbody.innerHTML = '';

  if (bids.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7">Нет добавленных заявок</td></tr>';
    return;
  }

  bids.forEach((bid, idx) => {
    let statusClass = '';
    if (bid.status === 'На проверке') statusClass = 'status-review';
    else if (bid.status === 'Согласована') statusClass = 'status-approved';
    else statusClass = 'status-rejected';

    // Файлы: через запятую
    let filesText = '—';
    if (bid.files && bid.files.length > 0) {
      filesText = bid.files.map(f => f.name).join(', ');
    }

    const row = tbody.insertRow();
    row.insertCell(0).innerText = bid.notice;
    row.insertCell(1).innerText = bid.company;
    row.insertCell(2).innerText = bid.nmck;
    row.insertCell(3).innerText = filesText;
    row.insertCell(4).innerHTML = `<span class="status ${statusClass}">${bid.status}</span>`;
    row.insertCell(5).innerText = bid.deadline;

    const delCell = row.insertCell(6);
    const delBtn = document.createElement('button');
    delBtn.innerText = 'Удалить';
    delBtn.classList.add('delete-btn');
    delBtn.onclick = () => {
      bids.splice(idx, 1);
      renderTable();
    };
    delCell.appendChild(delBtn);
  });
}

function addBid() {
  const notice = document.getElementById('notice').value.trim();
  const company = document.getElementById('company').value.trim();
  const nmck = parseInt(document.getElementById('nmck').value, 10) || 0;
  const deadline = document.getElementById('deadline').value;
  const status = document.getElementById('status').value;
  const fileInput = document.getElementById('files');

  if (!notice || !company) {
    alert('Заполните номер извещения и организацию');
    return;
  }
  if (!deadline) {
    alert('Укажите срок подачи');
    return;
  }
  if (fileInput.files.length === 0) {
    alert('Выберите хотя бы один файл');
    return;
  }

  // Сохраняем ВСЕ выбранные файлы
  const files = [];
  for (let i = 0; i < fileInput.files.length; i++) {
    files.push(fileInput.files[i]);
  }

  bids.push({
    notice: notice,
    company: company,
    nmck: nmck,
    deadline: deadline,
    status: status,
    files: files
  });

  renderTable();

  // Очистка формы
  document.getElementById('notice').value = '';
  document.getElementById('company').value = '';
  document.getElementById('nmck').value = '';
  document.getElementById('deadline').value = '';
  document.getElementById('status').selectedIndex = 0;
  document.getElementById('files').value = '';
}

document.getElementById('addBtn').addEventListener('click', addBid);
