-- ==========================================
-- Event Collection: структура базы данных
-- Четыре таблицы предметной области:
-- пользователи, мероприятия, посещения, оценки
-- ==========================================

-- Пользователи сервиса
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Мероприятия: название, категория и дата проведения.
-- Поле title_lower хранит название в нижнем регистре:
-- функция LOWER в SQLite не работает с кириллицей,
-- поэтому поиск без учета регистра выполняется по нему
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    title_lower TEXT NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL
);

-- Посещения: пользователь побывал на мероприятии
CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Оценки: один балл от 1 до 5 за одно посещение
CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY,
    visit_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (visit_id) REFERENCES visits(id)
);
