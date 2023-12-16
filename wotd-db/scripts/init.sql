CREATE TABLE IF NOT EXISTS language (
  language_uuid VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100)
);

INSERT INTO language (language_uuid, name) VALUES
  ('DE', 'German'),
  ('EN', 'English');


CREATE TABLE IF NOT EXISTS language_default (
  language_default_id SERIAL PRIMARY KEY,
  dict_from_language_uuid VARCHAR(50),
  dict_to_language_uuid VARCHAR(50),
  FOREIGN KEY (dict_from_language_uuid) REFERENCES language(language_uuid),
  FOREIGN KEY (dict_to_language_uuid) REFERENCES language(language_uuid)
);

INSERT INTO language_default (dict_from_language_uuid, dict_to_language_uuid) VALUES
  ('EN', 'DE');


CREATE TABLE dict_request (
  dict_request_id SERIAL PRIMARY KEY,
  from_language_uuid VARCHAR(50),
  to_language_uuid VARCHAR(50),
  input varchar(100) UNIQUE,
  FOREIGN KEY (from_language_uuid) REFERENCES language(language_uuid),
  FOREIGN KEY (to_language_uuid) REFERENCES language(language_uuid)
);
