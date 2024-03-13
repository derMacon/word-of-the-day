CREATE TABLE IF NOT EXISTS language (
  language_uuid VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

INSERT INTO language (language_uuid, name) VALUES
  ('DE', 'German'),
  ('EN', 'English');


CREATE TABLE IF NOT EXISTS language_default (
  language_default_id SERIAL PRIMARY KEY,
  dict_from_language_uuid VARCHAR(50) NOT NULL,
  dict_to_language_uuid VARCHAR(50) NOT NULL,
  FOREIGN KEY (dict_from_language_uuid) REFERENCES language(language_uuid),
  FOREIGN KEY (dict_to_language_uuid) REFERENCES language(language_uuid)
);

INSERT INTO language_default (dict_from_language_uuid, dict_to_language_uuid) VALUES
  ('EN', 'DE');

CREATE TABLE IF NOT EXISTS dict_options_item (
  dict_options_item_id SERIAL PRIMARY KEY,
  input VARCHAR(100) NOT NULL,
  output VARCHAR(100) NOT NULL,
  selected BOOLEAN NOT NULL,
  status VARCHAR(100) NOT NULL,
  option_response_ts timestamp NOT NULL
);
