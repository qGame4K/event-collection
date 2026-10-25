-- ==========================================
-- Event Collection: SQL-запросы проекта
-- Все запросы проверены в SQLite CLI на базе
-- data/event_collection.sqlite
-- Знак ? — место для значения, которое приложение
-- передает параметром
-- ==========================================

-- 1. Список мероприятий по дате (страница /events/)
SELECT
    id,
    title,
    category,
    date,
    strftime('%d.%m.%Y', date) AS date_display
FROM events
ORDER BY date;

-- 2. Список пользователей по имени
SELECT
    id,
    name,
    email
FROM users
ORDER BY name;

-- 3. Поиск мероприятий по части названия (страница /events/search/).
--    Сравнение идет по полю title_lower, поэтому регистр не важен:
--    приложение передает запрос пользователя в нижнем регистре
SELECT
    id,
    title,
    category,
    strftime('%d.%m.%Y', date) AS date_display
FROM events
WHERE title_lower LIKE ?
ORDER BY date;

-- 4. Мероприятия выбранной категории
SELECT
    id,
    title,
    strftime('%d.%m.%Y', date) AS date_display
FROM events
WHERE category = ?
ORDER BY date;

-- 5. Мероприятия, которые уже прошли
SELECT
    title,
    date
FROM events
WHERE date <= date('now')
ORDER BY date DESC;

-- 6. Список категорий без повторов (для формы поиска)
SELECT DISTINCT category
FROM events
ORDER BY category;

-- 7. Карточка мероприятия с числом посещений и средней оценкой
--    (страница /events/<id>/)
SELECT
    events.id,
    events.title,
    events.category,
    strftime('%d.%m.%Y', events.date) AS date_display,
    events.date <= date('now') AS is_past,
    COUNT(visits.id) AS visits_count,
    ROUND(AVG(ratings.score), 1) AS average_score
FROM events
LEFT JOIN visits
    ON visits.event_id = events.id
LEFT JOIN ratings
    ON ratings.visit_id = visits.id
WHERE events.id = ?
GROUP BY events.id;

-- 8. Посещения с пользователем, мероприятием и оценкой
--    (страница /visits/)
SELECT
    visits.id,
    users.name AS user_name,
    events.title AS event_title,
    strftime('%d.%m.%Y', events.date) AS date_display,
    ratings.score
FROM visits
JOIN users
    ON visits.user_id = users.id
JOIN events
    ON visits.event_id = events.id
LEFT JOIN ratings
    ON ratings.visit_id = visits.id
ORDER BY events.date DESC;

-- 9. Карточка посещения по номеру (страница /visits/<id>/)
SELECT
    visits.id,
    users.name AS user_name,
    users.email AS user_email,
    events.id AS event_id,
    events.title AS event_title,
    events.category,
    strftime('%d.%m.%Y', events.date) AS date_display,
    ratings.score
FROM visits
JOIN users
    ON visits.user_id = users.id
JOIN events
    ON visits.event_id = events.id
LEFT JOIN ratings
    ON ratings.visit_id = visits.id
WHERE visits.id = ?;

-- 10. Коллекция выбранного пользователя
SELECT
    events.title,
    strftime('%d.%m.%Y', events.date) AS date_display,
    ratings.score
FROM visits
JOIN events
    ON visits.event_id = events.id
LEFT JOIN ratings
    ON ratings.visit_id = visits.id
WHERE visits.user_id = ?
ORDER BY events.date DESC;

-- 11. Общие показатели проекта (страница /visits/statistics/)
SELECT
    (SELECT COUNT(*) FROM users) AS users_count,
    (SELECT COUNT(*) FROM events) AS events_count,
    (SELECT COUNT(*) FROM visits) AS visits_count,
    (SELECT ROUND(AVG(score), 1) FROM ratings) AS average_score;

-- 12. Количество посещений и средняя оценка по категориям
SELECT
    events.category,
    COUNT(visits.id) AS visits_count,
    ROUND(AVG(ratings.score), 1) AS average_score
FROM events
LEFT JOIN visits
    ON visits.event_id = events.id
LEFT JOIN ratings
    ON ratings.visit_id = visits.id
GROUP BY events.category
ORDER BY visits_count DESC;

-- 13. Категории, в которых больше заданного числа посещений
SELECT
    events.category,
    COUNT(visits.id) AS visits_count
FROM events
JOIN visits
    ON visits.event_id = events.id
GROUP BY events.category
HAVING COUNT(visits.id) > ?
ORDER BY visits_count DESC;

-- 14. Самые посещаемые мероприятия (первые три)
SELECT
    events.title,
    COUNT(visits.id) AS visits_count
FROM events
JOIN visits
    ON visits.event_id = events.id
GROUP BY events.id, events.title
ORDER BY visits_count DESC
LIMIT 3;

-- 15. Мероприятия, которых еще нет в коллекции пользователя
SELECT
    events.id,
    events.title,
    strftime('%d.%m.%Y', events.date) AS date_display
FROM events
WHERE events.id NOT IN (
    SELECT visits.event_id
    FROM visits
    WHERE visits.user_id = ?
)
ORDER BY events.date;

-- 16. Посещения без оценки (проверка на NULL)
SELECT
    visits.id,
    events.title
FROM visits
JOIN events
    ON visits.event_id = events.id
LEFT JOIN ratings
    ON ratings.visit_id = visits.id
WHERE ratings.score IS NULL
ORDER BY visits.id;
