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


CREATE TABLE IF NOT EXISTS dict_request (
  dict_request_id SERIAL PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  from_language_uuid VARCHAR(50) NOT NULL,
  to_language_uuid VARCHAR(50) NOT NULL,
  input varchar(100) NOT NULL,
  dict_request_ts timestamp, 
  FOREIGN KEY (from_language_uuid) REFERENCES language(language_uuid),
  FOREIGN KEY (to_language_uuid) REFERENCES language(language_uuid)
);

CREATE TABLE IF NOT EXISTS dict_options_response (
  dict_options_response_id SERIAL PRIMARY KEY,
  dict_request_id INTEGER,
  status VARCHAR(100),
  options_response_ts timestamp
);

CREATE TABLE IF NOT EXISTS dict_options_item (
  dict_options_item_id SERIAL PRIMARY KEY,
  dict_options_response_id INTEGER NOT NULL,
  input VARCHAR(100),
  output VARCHAR(100),
  FOREIGN KEY (dict_options_response_id) REFERENCES dict_options_response(dict_options_response_id)
);
