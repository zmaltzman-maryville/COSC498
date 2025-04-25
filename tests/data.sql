INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO package (user_id, user_description, recipient, tracking_number,
carrier, current_status, order_date, delivery_date, delivered)
VALUES
  (1, 'Box 1', NULL, '123456', 'USPS', 'In Transit', '04/01/25', NULL, NULL),
  (1, 'Box 2', NULL, '1Z998877', 'UPS', 'In Transit', '04/02/25', NULL, NULL),
  (1, 'Box 3', 'Me', '741852', 'FedEx', 'Delivered', '04/04/25', '04/08/25', 1);