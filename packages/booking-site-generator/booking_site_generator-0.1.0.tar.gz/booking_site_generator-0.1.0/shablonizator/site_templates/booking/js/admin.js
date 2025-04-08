document.addEventListener('DOMContentLoaded', function() {
    // Проверка авторизации администратора
    const isAdminLoggedIn = localStorage.getItem('isAdminLoggedIn');
    if (!isAdminLoggedIn) {
        window.location.href = 'login.html';
        return;
    }
    
    // Получаем элементы
    const adminRequestsTable = document.getElementById('admin-requests-table');
    const searchInput = document.getElementById('search-requests');
    const filterStatus = document.getElementById('filter-status');
    
    // Загружаем все заявки
    loadAllRequests();
    
    // Обработчики событий фильтрации и поиска
    if (searchInput) {
        searchInput.addEventListener('input', filterRequests);
    }
    
    if (filterStatus) {
        filterStatus.addEventListener('change', filterRequests);
    }
    
    // Функция загрузки всех заявок
    function loadAllRequests() {
        // Получаем заявки из localStorage
        const allRequests = JSON.parse(localStorage.getItem('itemRequests') || '[]');
        
        // Сортируем заявки (сначала новые, затем подтвержденные, затем отклоненные)
        allRequests.sort((a, b) => {
            // Сначала сортируем по статусу
            const statusOrder = { 'new': 0, 'confirmed': 1, 'rejected': 2 };
            const statusDiff = statusOrder[a.status] - statusOrder[b.status];
            
            // Если статусы одинаковые, сортируем по дате создания (сначала новые)
            if (statusDiff === 0) {
                return new Date(b.createdAt) - new Date(a.createdAt);
            }
            
            return statusDiff;
        });
        
        // Отображаем заявки
        displayRequests(allRequests);
    }
    
    // Функция отображения заявок в админ-панели
    function displayRequests(requests) {
        if (!adminRequestsTable) {
            console.error('Таблица заявок не найдена');
            return;
        }
        
        // Очищаем таблицу, сохраняя заголовок
        const tableHeader = adminRequestsTable.querySelector('thead');
        if (tableHeader) {
            adminRequestsTable.innerHTML = '';
            adminRequestsTable.appendChild(tableHeader);
        } else {
            adminRequestsTable.innerHTML = `
                <thead>
                    <tr>
                        <th>№</th>
                        <th>ФИО</th>
                        <th>Телефон</th>
                        <th>Email</th>
                        <th>Товар</th>
                        <th>Дата</th>
                        <th>Статус</th>
                        <th>Действия</th>
                    </tr>
                </thead>
            `;
        }
        
        // Создаем тело таблицы
        const tableBody = document.createElement('tbody');
        
        // Если нет заявок, показываем сообщение
        if (requests.length === 0) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.colSpan = 8;
            cell.textContent = 'Нет заявок';
            cell.style.textAlign = 'center';
            row.appendChild(cell);
            tableBody.appendChild(row);
        } else {
            // Заполняем таблицу данными
            requests.forEach(request => {
                const row = document.createElement('tr');
                
                // ID
                const idCell = document.createElement('td');
                idCell.textContent = request.id;
                
                // ФИО
                const nameCell = document.createElement('td');
                nameCell.textContent = request.userName || 'Н/Д';
                
                // Телефон
                const phoneCell = document.createElement('td');
                phoneCell.textContent = request.phone || 'Н/Д';
                
                // Email
                const emailCell = document.createElement('td');
                emailCell.textContent = request.userEmail || 'Н/Д';
                
                // Товар
                const itemCell = document.createElement('td');
                itemCell.textContent = request.item || 'Н/Д';
                
                // Дата
                const dateCell = document.createElement('td');
                dateCell.textContent = request.date || 'Н/Д';
                
                // Статус
                const statusCell = document.createElement('td');
                const statusSelect = document.createElement('select');
                statusSelect.className = 'status-select';
                statusSelect.dataset.id = request.id;
                
                // Добавляем опции статуса
                const statuses = [
                    { value: 'new', text: 'Новая' },
                    { value: 'confirmed', text: 'Подтверждена' },
                    { value: 'rejected', text: 'Отклонена' }
                ];
                
                statuses.forEach(status => {
                    const option = document.createElement('option');
                    option.value = status.value;
                    option.textContent = status.text;
                    if (request.status === status.value) {
                        option.selected = true;
                    }
                    statusSelect.appendChild(option);
                });
                
                statusCell.appendChild(statusSelect);
                
                // Кнопка сохранения
                const actionsCell = document.createElement('td');
                const saveButton = document.createElement('button');
                saveButton.className = 'btn-save';
                saveButton.dataset.id = request.id;
                saveButton.textContent = 'Сохранить';
                
                // Обработчик клика по кнопке сохранения
                saveButton.addEventListener('click', function() {
                    const requestId = parseInt(this.dataset.id);
                    const newStatus = statusSelect.value;
                    updateRequestStatus(requestId, newStatus);
                });
                
                actionsCell.appendChild(saveButton);
                
                // Добавляем ячейки в строку
                row.appendChild(idCell);
                row.appendChild(nameCell);
                row.appendChild(phoneCell);
                row.appendChild(emailCell);
                row.appendChild(itemCell);
                row.appendChild(dateCell);
                row.appendChild(statusCell);
                row.appendChild(actionsCell);
                
                // Добавляем строку в тело таблицы
                tableBody.appendChild(row);
            });
        }
        
        // Добавляем тело таблицы в таблицу
        adminRequestsTable.appendChild(tableBody);
    }
    
    // Функция обновления статуса заявки
    function updateRequestStatus(requestId, newStatus) {
        // Получаем все заявки
        const allRequests = JSON.parse(localStorage.getItem('itemRequests') || '[]');
        
        // Находим заявку по ID
        const requestIndex = allRequests.findIndex(request => request.id === requestId);
        
        if (requestIndex === -1) {
            showToast('Заявка не найдена', 'error');
            return;
        }
        
        // Обновляем статус
        allRequests[requestIndex].status = newStatus;
        
        // Сохраняем обновленные данные
        localStorage.setItem('itemRequests', JSON.stringify(allRequests));
        
        // Показываем уведомление
        showToast('Статус заявки обновлен', 'success');
    }
    
    // Функция фильтрации заявок
    function filterRequests() {
        const searchQuery = searchInput ? searchInput.value.toLowerCase() : '';
        const statusFilter = filterStatus ? filterStatus.value : 'all';
        
        // Получаем все заявки
        const allRequests = JSON.parse(localStorage.getItem('itemRequests') || '[]');
        
        // Применяем фильтры
        const filteredRequests = allRequests.filter(request => {
            // Фильтр по статусу
            if (statusFilter !== 'all' && request.status !== statusFilter) {
                return false;
            }
            
            // Фильтр по поисковому запросу
            if (searchQuery) {
                const userName = (request.userName || '').toLowerCase();
                const itemName = (request.item || '').toLowerCase();
                const email = (request.userEmail || '').toLowerCase();
                
                return userName.includes(searchQuery) || 
                       itemName.includes(searchQuery) || 
                       email.includes(searchQuery);
            }
            
            return true;
        });
        
        // Отображаем отфильтрованные заявки
        displayRequests(filteredRequests);
    }
    
    // Функция показа уведомления
    function showToast(message, type = 'success') {
        // Создаем элемент уведомления
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        // Добавляем на страницу
        document.body.appendChild(toast);
        
        // Показываем уведомление
        setTimeout(() => {
            toast.classList.add('toast-visible');
        }, 100);
        
        // Скрываем и удаляем через 3 секунды
        setTimeout(() => {
            toast.classList.remove('toast-visible');
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }
});