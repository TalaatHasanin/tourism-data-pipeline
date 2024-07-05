use warehouse easy_tour_wh;
use database easy_tour_db;
use schema easy_tour_sch;

select * from aitrip_places;
select * from customtrip_places;
select * from tourguidetrip_places;

-- Most 5 Popular Places (Across All Trip Types)
SELECT p.place_name, COUNT(*) AS visit_count
FROM (
  SELECT place_name
  FROM aitrip_places
  WHERE place_name IS NOT NULL
  UNION ALL
  SELECT place_name
  FROM customtrip_places
  UNION ALL
  SELECT place_name
  FROM tourguidetrip_places
) AS p
GROUP BY p.place_name
ORDER BY visit_count DESC
LIMIT 5;

-- Average Custom Trip price range
SELECT AVG(price_range)
FROM customtrip_places;

SELECT category, COUNT(*) AS count
FROM aitrip_places
WHERE category IS NOT NULL
GROUP BY category
ORDER BY count DESC
LIMIT 1;



-- number of all trips created in application
SELECT COUNT(*) AS all_trips
FROM (
  SELECT place_name
  FROM aitrip_places
  UNION ALL
  SELECT place_name
  FROM customtrip_places
  UNION ALL
  SELECT place_name
  FROM tourguidetrip_places
);

-- Average Custom Trip Length
SELECT AVG(day_count)
FROM (SELECT customtrip_id, COUNT(DISTINCT day_name)
AS day_count FROM customtrip_days GROUP BY customtrip_id) AS day_counts;


SELECT p.place_name,
       SUM(CASE WHEN p.source = 'AI' THEN 1 ELSE 0 END) AS ai_trips,
       SUM(CASE WHEN p.source = 'Custom' THEN 1 ELSE 0 END) AS custom_trips
FROM (
  SELECT place_name, 'AI' AS source
  FROM aitrip_places
  WHERE place_name IS NOT NULL
  UNION ALL
  SELECT place_name, 'Custom' AS source
  FROM customtrip_places
  WHERE place_name IS NOT NULL
) AS p
GROUP BY p.place_name;


SELECT t.USER_NAME, t.EMAIL, t.PHONE_NUMBER, COUNT(*) AS ai_trip_count
FROM tourists AS t
JOIN aitrips AS a ON t._ID = a.TOURIST_ID
GROUP BY t.USER_NAME, t.EMAIL, t.PHONE_NUMBER
ORDER BY ai_trip_count DESC;


SELECT t.USER_NAME, t.EMAIL, t.PHONE_NUMBER, COUNT(*) AS custom_trip_count
FROM tourists AS t
JOIN customtrips AS c ON t._ID = c.tourist_id
GROUP BY t.USER_NAME, t.EMAIL, t.PHONE_NUMBER
ORDER BY custom_trip_count DESC;


SELECT p.activity, COUNT(*) as activity_count
FROM (
    SELECT activity FROM aitrip_places
    UNION ALL
    SELECT activity FROM customtrip_places
    UNION ALL
    SELECT activity FROM tourguidetrip_places
) as p
GROUP BY p.activity
ORDER BY activity_count DESC;


SELECT _id AS tourguidetrip_id,
       standard AS standard_price,
       luxury AS luxury_price,
       vip AS vip_price,
       current_travelers_no AS bookings -- Assuming this represents bookings
FROM tourguidetrips
ORDER BY bookings DESC;




SELECT
    a._ID AS trip_id,
    a.TOURIST_ID,
    a.STATUS AS trip_status,
    a.TITLE AS trip_title,
    a."from",
    a."to",
    p._id AS place_id,
    p.place_name,
    p.day_number,
    p.longitude,
    p.latitude,
    p.activity,
    p.category
FROM aitrips AS a
JOIN aitrip_places AS p ON a._ID = p.aitrip_id;



