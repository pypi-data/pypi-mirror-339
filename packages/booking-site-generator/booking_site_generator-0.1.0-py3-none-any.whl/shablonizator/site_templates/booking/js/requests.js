document.addEventListener('DOMContentLoaded', function() {
    // Проверка авторизации
    if (typeof window.checkAuth === 'function') {
        window.checkAuth();
    } else {
        // Если функция не определена, реализуем свою проверку
        const isLoggedIn = localStorage.getItem('isLoggedIn');
        if (!isLoggedIn) {
            window.location.href = 'login.html';
            return;
        }
    }
    
    // Получаем элементы
    const requestsTable = document.getElementById('requests-table');
    const noRequestsDiv = document.getElementById('no-requests');
    
    // Проверяем, есть ли элементы на странице
    if (!requestsTable || !noRequestsDiv) {
        console.error('Элементы для отображения заявок не найдены');
        return;
    }
    
    // Загрузка заявок пользователя
    loadUserRequests();
    
    // Функция загрузки заявок пользователя
    function loadUserRequests() {
        // Получаем email текущего пользователя
        const userEmail = localStorage.getItem('userEmail');
        
        // Получаем все заявки из localStorage
        const allRequests = JSON.parse(localStorage.getItem('itemRequests') || '[]');
        
        // Фильтруем заявки текущего пользователя
        const userRequests = allRequests.filter(request => request.userEmail === userEmail);
        
        // Сортируем заявки по дате создания (сначала новые)
        userRequests.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        
        // Отображаем заявки
        displayRequests(userRequests);
    }
    
    // Функция отображения заявок
    function displayRequests(requests) {
        if (!requests || requests.length === 0) {
            showNoRequests();
            return;
        }
        
        // Показываем таблицу и скрываем сообщение об отсутствии заявок
        requestsTable.style.display = 'table';
        noRequestsDiv.style.display = 'none';
        
        // Очищаем текущую таблицу, сохраняя заголовок
        const tableHeader = requestsTable.querySelector('thead');
        if (tableHeader) {
            requestsTable.innerHTML = '';
            requestsTable.appendChild(tableHeader);
        } else {
            requestsTable.innerHTML = `
                <thead>
                    <tr>
                        <th>№</th>
                        <th>Товар</th>
                        <th>Дата бронирования</th>
                        <th>Статус</th>
                    </tr>
                </thead>
            `;
        }
        
        // Создаем тело таблицы
        const tableBody = document.createElement('tbody');
        
        // Заполняем таблицу данными
        requests.forEach(request => {
            const row = document.createElement('tr');
            
            // Создаем ячейки таблицы
            const idCell = document.createElement('td');
            idCell.textContent = request.id;
            
            const itemCell = document.createElement('td');
            itemCell.textContent = request.item;
            
            const dateCell = document.createElement('td');
            dateCell.textContent = request.date;
            
            const statusCell = document.createElement('td');
            const statusSpan = document.createElement('span');
            statusSpan.className = 'status';
            
            // Устанавливаем класс и текст статуса
            if (request.status === 'new') {
                statusSpan.classList.add('status-new');
                statusSpan.textContent = 'Новая';
            } else if (request.status === 'confirmed') {
                statusSpan.classList.add('status-confirmed');
                statusSpan.textContent = 'Подтверждена';
            } else if (request.status === 'rejected') {
                statusSpan.classList.add('status-rejected');
                statusSpan.textContent = 'Отклонена';
            }
            
            statusCell.appendChild(statusSpan);
            
            // Добавляем ячейки в строку
            row.appendChild(idCell);
            row.appendChild(itemCell);
            row.appendChild(dateCell);
            row.appendChild(statusCell);
            
            // Добавляем строку в тело таблицы
            tableBody.appendChild(row);
        });
        
        // Добавляем тело таблицы в таблицу
        requestsTable.appendChild(tableBody);
    }
    
    // Функция отображения сообщения об отсутствии заявок
    function showNoRequests() {
        requestsTable.style.display = 'none';
        noRequestsDiv.style.display = 'block';
    }
});