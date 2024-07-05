use warehouse easy_tour_wh;
use database easy_tour_db;

CREATE OR REPLACE TABLE analysis.popular_five_places_all_trips
AS (
SELECT p.place_name, COUNT(*) AS visit_count
FROM (
  SELECT place_name
  FROM easy_tour_sch.aitrip_places
  WHERE place_name IS NOT NULL
  UNION ALL
  SELECT place_name
  FROM easy_tour_sch.customtrip_places
  WHERE place_name IS NOT NULL
  UNION ALL
  SELECT place_name
  FROM easy_tour_sch.tourguidetrip_places
  WHERE place_name IS NOT NULL
) AS p
GROUP BY p.place_name
ORDER BY visit_count DESC
LIMIT 5
);

CREATE OR REPLACE TABLE analysis.avg_customtrips_price
AS (
-- Average Custom Trip price range
SELECT AVG(price_range) AS avg_price
FROM easy_tour_sch.customtrip_places
);


CREATE OR REPLACE TABLE analysis.count_all_trips
AS (
-- number of all trips created in application
SELECT COUNT(*) AS all_trips
FROM (
  SELECT place_name
  FROM easy_tour_sch.aitrip_places
  UNION ALL
  SELECT place_name
  FROM easy_tour_sch.customtrip_places
  UNION ALL
  SELECT place_name
  FROM easy_tour_sch.tourguidetrip_places
)
);

CREATE OR REPLACE TABLE analysis.most_used_category_aitrips
AS (
SELECT category
FROM (
SELECT category, COUNT(*) AS count
FROM easy_tour_sch.aitrip_places
WHERE category IS NOT NULL
GROUP BY category
ORDER BY count DESC
LIMIT 1
) AS top_category
);

CREATE OR REPLACE TABLE analysis.most_used_category_customtrips
AS (
SELECT category
FROM (
SELECT category, COUNT(*) AS count
FROM easy_tour_sch.customtrip_places
WHERE category IS NOT NULL
GROUP BY category
ORDER BY count DESC
LIMIT 1
) AS top_category
);


CREATE OR REPLACE TABLE analysis.popular_five_place_type_tourguidetrips
AS (
SELECT place_type, COUNT(*) AS count
FROM easy_tour_sch.tourguidetrip_places
WHERE place_type IS NOT NULL
GROUP BY place_type
ORDER BY count DESC
LIMIT 5
);


CREATE OR REPLACE TABLE analysis.avg_day_count (
    average_day_count FLOAT
) AS
SELECT AVG(day_count) AS average_day_count
FROM (
    SELECT customtrip_id, COUNT(DISTINCT day_name) AS day_count
    FROM easy_tour_sch.customtrip_days
    GROUP BY customtrip_id
) AS day_counts;


CREATE OR REPLACE TABLE analysis.popular_five_governorates_tourguidetrips
AS (
SELECT place_name, COUNT(*) AS count
FROM easy_tour_sch.tourguidetrip_places
WHERE place_name IS NOT NULL
GROUP BY place_name
ORDER BY count DESC
LIMIT 5
);