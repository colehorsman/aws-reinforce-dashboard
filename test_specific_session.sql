-- Test the specific session that user reported
SELECT 
    title,
    CASE WHEN key_points IS NOT NULL AND length(key_points) > 10 
         THEN 'Has Enhanced Content' 
         ELSE 'Missing Content' END as key_points_status,
    CASE WHEN technical_details IS NOT NULL AND length(technical_details) > 10 
         THEN 'Has Enhanced Content' 
         ELSE 'Missing Content' END as tech_details_status,
    substring(key_points, 1, 100) as key_points_preview
FROM summaries 
WHERE title ILIKE '%5 ways generative AI can enhance cybersecurity%' 
AND year = 2024;
