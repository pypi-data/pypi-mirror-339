DROP VIEW IF EXISTS "unaccent_verses";

-- This table is for searching verses without diacritics.
CREATE VIEW "unaccent_verses" AS
SELECT 
  "id",
  "number",
  "chapter_id",
  "part_id",
  "group_id",
  "quarter_id",
  "page_id",
  REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("content", 'ۜ', ''), 'ۥ', ''), 'ۦ', ''), 'ۚ', ''), 'ٍ', ''), 'ٌ', ''), 'ً', ''), 'ۢ', ''), '۟', ''), 'ۗ', ''), 'ۖ', ''), 'ۭ', ''), 'ۛ', ''), 'ٱ', 'ا'), 'ٰ', ''), 'ٓ', ''), 'ّ', ''), 'ْ', ''), 'ِ', ''), 'ُ', ''), 'َ', '') as "content"
FROM "verses";
