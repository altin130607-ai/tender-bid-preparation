// Массив заявок
let bids = [];

// Функция отрисовки таблицы
function renderTable() {
  const tbody = document.getElementById('bidsBody');
  tbody.innerHTML = '';

  if (bids.length === 0) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="6">Нет добавленных заявок</td></tr>';
    return;
  }

  bids.forEach((bid, index) => {
    const row = tbody.insertRow();

    let statusClass = '';
    if (bid.status === 'На проверке') statusClass = 'status-review';
    else if (bid.status === 'Согласована') statusClass = 'status-approved';
    else if (bid.status === 'Отклонена') statusClass = 'status-rejected';

    row.insertCell(0).innerText = bid.noticeNumber;
    row.insertCell(1).innerText = bid.company;
    row.insertCell(2).innerText = Number(bid.nmck).toLocaleString('ru-RU');
    row.insertCell(3).innerHTML = <span class="status ${statusClass}">${bid.status}</span>;
    row.insertCell(4).innerText = bid.deadline;

    const actionsCell = row.insertCell(5);
    const delBtn = document.createElement('button');
    delBtn.innerText = 'Удалить';
    delBtn.className = 'delete-btn';
    delBtn.onclick = () => {
      bids.splice(index, 1);
      renderTable();
    };
    actionsCell.appendChild(delBtn);
  });
}

// Добавление заявки
function addBid() {
  const noticeNumber = document.getElementById('noticeNumber').value.trim();
  const company = document.getElementById('company').value.trim();
  let nmck = parseInt(document.getElementById('nmck').value, 10);
  const status = document.getElementById('status').value;
  let deadline = document.getElementById('deadline').value;

  if (!noticeNumber || !company) {
    alert('Заполните номер извещения и организацию');
    return;
  }
  if (isNaN(nmck)) nmck = 0;
  if (!deadline) {
    deadline = new Date().toISOString().slice(0,10);
  }

  bids.push({
    noticeNumber: noticeNumber,
    company: company,
    nmck: nmck,
    status: status,
    deadline: deadline
  });

  renderTable();

  // Очистка полей
  document.getElementById('noticeNumber').value = '';
  document.getElementById('company').value = '';
  document.getElementById('nmck').value = '';
  document.getElementById('status').selectedIndex = 0;
  document.getElementById('deadline').value = '';
  document.getElementById('noticeNumber').focus();
}

// Навешиваем обработчики
document.getElementById('addBtn').addEventListener('click', addBid);

// Добавляем Enter на поля
const inputs = ['noticeNumber', 'company', 'nmck', 'deadline'];
inputs.forEach(id => {
  const el = document.getElementById(id);
  if (el) {
    el.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') addBid();
    });
  }
});