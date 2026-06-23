-- sql_practice/queries.sql
-- SQL practice queries on spam dataset

-- 1. View sample data
SELECT * FROM messages LIMIT 10;

-- 2. Count spam vs ham
SELECT label, COUNT(*) AS total
FROM messages
GROUP BY label;

-- 3. Find longest messages
SELECT message, msg_length
FROM messages
ORDER BY msg_length DESC
LIMIT 5;

-- 4. Average message length per label
SELECT label, AVG(msg_length) AS avg_length
FROM messages
GROUP BY label;

-- 5. Search for keyword in spam
SELECT message
FROM messages
WHERE label = 'spam' AND message ILIKE '%free%'
LIMIT 10;

-- 6. Percentage of spam
SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE label = 'spam') / COUNT(*), 2) AS spam_percentage
FROM messages;

-- 7. Bucket by length
SELECT
  CASE
    WHEN msg_length < 50 THEN 'short'
    WHEN msg_length < 100 THEN 'medium'
    ELSE 'long'
  END AS length_bucket,
  label, COUNT(*) AS total
FROM messages
GROUP BY length_bucket, label
ORDER BY length_bucket;

-- 8. Rank messages by length within label
SELECT label, message, msg_length,
  RANK() OVER (PARTITION BY label ORDER BY msg_length DESC) AS length_rank
FROM messages
LIMIT 20;

-- 9. Find duplicate messages
SELECT message, COUNT(*) AS occurrences
FROM messages
GROUP BY message
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;

-- 10. Standard deviation of message length
SELECT label,
  ROUND(AVG(msg_length), 2) AS avg_len,
  ROUND(STDDEV(msg_length), 2) AS std_dev
FROM messages
GROUP BY label;