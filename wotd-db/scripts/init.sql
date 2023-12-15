CREATE TABLE IF NOT EXISTS language (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  abbreviation VARCHAR(100)
);

INSERT INTO language (id, name, abbreviation) VALUES
  (1, 'German', 'DE'),
  (2, 'English', 'EN');


CREATE TABLE IF NOT EXISTS language_defaults (
  id SERIAL PRIMARY KEY,
  dict_from_language_id integer,
  dict_to_language_id integer,
  FOREIGN KEY (dict_from_language_id) REFERENCES language(id),
  FOREIGN KEY (dict_to_language_id) REFERENCES language(id)
);

INSERT INTO language_defaults (dict_from_language_id, dict_to_language_id) VALUES
  (1, 2);


-- CREATE TABLE dict_request (
--   id SERIAL PRIMARY KEY,
--   name VARCHAR(100),
--   age INTEGER
-- );
