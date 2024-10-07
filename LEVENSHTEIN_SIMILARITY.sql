DELIMITER $$

CREATE FUNCTION LEVENSHTEIN_SIMILARITY(s1 VARCHAR(255), s2 VARCHAR(255))
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
  DECLARE s1_len, s2_len, i, j, cost INT;
  DECLARE d BLOB;
  DECLARE distance INT;
  DECLARE max_len INT;
  DECLARE similarity DECIMAL(5,2);

  -- Get the lengths of both strings (supports Arabic and other UTF-8 languages)
  SET s1_len = CHAR_LENGTH(s1);
  SET s2_len = CHAR_LENGTH(s2);

  -- If both strings are empty, return 100 (exact match)
  IF s1_len = 0 AND s2_len = 0 THEN
    RETURN 100.00;
  END IF;

  -- If one of the strings is empty, return 0 (no similarity)
  IF s1_len = 0 OR s2_len = 0 THEN
    RETURN 0.00;
  END IF;

  -- Create a distance matrix
  SET d = REPEAT(CHAR(0), (s1_len + 1) * (s2_len + 1));

  -- Initialize the first row and column of the matrix
  SET i = 0;
  WHILE i <= s1_len DO
    SET d = INSERT(d, (i * (s2_len + 1)) + 1, 1, CHAR(i));
    SET i = i + 1;
  END WHILE;

  SET j = 0;
  WHILE j <= s2_len DO
    SET d = INSERT(d, j + 1, 1, CHAR(j));
    SET j = j + 1;
  END WHILE;

  -- Compute the Levenshtein distance
  SET i = 1;
  WHILE i <= s1_len DO
    SET j = 1;
    WHILE j <= s2_len DO
      IF SUBSTRING(s1, i, 1) = SUBSTRING(s2, j, 1) THEN
        SET cost = 0;
      ELSE
        SET cost = 1;
      END IF;

      SET d = INSERT(d, ((i * (s2_len + 1)) + j) + 1, 1, CHAR(
          LEAST(
            ORD(SUBSTRING(d, ((i - 1) * (s2_len + 1)) + j + 1, 1)) + 1,
            ORD(SUBSTRING(d, (i * (s2_len + 1)) + j, 1)) + 1,
            ORD(SUBSTRING(d, ((i - 1) * (s2_len + 1)) + (j - 1) + 1, 1)) + cost
          )
        ));
      SET j = j + 1;
    END WHILE;
    SET i = i + 1;
  END WHILE;

  -- Calculate the Levenshtein distance
  SET distance = ORD(SUBSTRING(d, (s1_len * (s2_len + 1)) + s2_len + 1, 1));

  -- Find the maximum length between the two strings
  SET max_len = GREATEST(s1_len, s2_len);

  -- Calculate the similarity score
  SET similarity = (1 - distance / max_len) * 100;

  -- Return the similarity score
  RETURN similarity;
END$$

DELIMITER ;
