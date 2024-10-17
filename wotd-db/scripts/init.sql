SET TIMEZONE TO 'Europe/Berlin';

CREATE TABLE IF NOT EXISTS language (
  language_uuid VARCHAR(50) PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  enchant_key VARCHAR(100) NOT NULL
);

INSERT INTO language (language_uuid, full_name, enchant_key) VALUES
  ('DE', 'German', 'de_DE'),
  ('EN', 'English', 'en_US'),
  ('FR', 'French', 'fr_FR');

CREATE TABLE IF NOT EXISTS dict_options_item (
  dict_options_item_id SERIAL PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  deck VARCHAR(100) NOT NULL,
  input VARCHAR(1000) NOT NULL,
  output VARCHAR(1000) NOT NULL,
  selected BOOLEAN NOT NULL,
  status VARCHAR(100) NOT NULL,
  option_response_ts timestamp NOT NULL,
  CONSTRAINT unique_dict_option UNIQUE (deck, input, output)
);

CREATE TABLE IF NOT EXISTS dict_request (
  dict_request_id SERIAL PRIMARY KEY,
  username VARCHAR(100),
  from_language_uuid VARCHAR(50) NOT NULL,
  to_language_uuid VARCHAR(50) NOT NULL,
  FOREIGN KEY (from_language_uuid) REFERENCES language(language_uuid),
  FOREIGN KEY (to_language_uuid) REFERENCES language(language_uuid),
  input VARCHAR(1000) NOT NULL,
  dict_request_ts timestamp NOT NULL
);
