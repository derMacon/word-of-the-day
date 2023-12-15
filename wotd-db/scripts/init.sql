CREATE TABLE IF NOT EXISTS language (
  language_id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  abbreviation VARCHAR(100)
);

INSERT INTO language (language_id, name, abbreviation) VALUES
  (1, 'German', 'DE'),
  (2, 'English', 'EN');


CREATE TABLE IF NOT EXISTS language_default (
  language_default_id SERIAL PRIMARY KEY,
  dict_from_language_id integer,
  dict_to_language_id integer,
  FOREIGN KEY (dict_from_language_id) REFERENCES language(language_id),
  FOREIGN KEY (dict_to_language_id) REFERENCES language(language_id)
);

INSERT INTO language_default (dict_from_language_id, dict_to_language_id) VALUES
  (1, 2);


-- CREATE TABLE dict_request (
--   id SERIAL PRIMARY KEY,
--   name VARCHAR(100),
--   age INTEGER
-- );
