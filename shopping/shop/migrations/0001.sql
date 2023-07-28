BEGIN;
--
-- Create model Address
--
CREATE TABLE "addresses" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "country" varchar(50) NOT NULL,
    "city" varchar(30) NOT NULL,
    "street" varchar(40) NOT NULL,
    "house" varchar(5) NOT NULL,
    "building" smallint unsigned NULL CHECK ("building" >= 0),
    "apartment" smallint unsigned NOT NULL CHECK ("apartment" >= 0),
    "index" varchar(6) NOT NULL
);
--
-- Create model Basket
--
CREATE TABLE "baskets" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "total" decimal NOT NULL,
    "discount" smallint unsigned NULL CHECK ("discount" >= 0)
);
--
-- Create model BasketProduct
--
CREATE TABLE "products_baskets" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "quantity" smallint unsigned NOT NULL CHECK ("quantity" >= 0),
    "basket_id" bigint NOT NULL REFERENCES "baskets" ("id") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model Category
--
CREATE TABLE "categories" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL, "description" text NOT NULL, "image" varchar(100) NULL);
--
-- Create model Client
--
CREATE TABLE "clients" (
    "user_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "discount" smallint unsigned NULL CHECK ("discount" >= 0),
    "phone" varchar(15) NULL
);
--
-- Create model Delivery
--
CREATE TABLE "deliveries" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "method" varchar(20) NOT NULL);
--
-- Create model Status
--
CREATE TABLE "statuses" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(45) NOT NULL);
--
-- Create model Product
--
CREATE TABLE "products" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(255) NOT NULL,
    "price" decimal NOT NULL,
    "availability" smallint unsigned NOT NULL CHECK ("availability" >= 0),
    "image" varchar(100) NULL,
    "discount" smallint unsigned NOT NULL CHECK ("discount" >= 0),
    "category_id" bigint NOT NULL REFERENCES "categories" ("id") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model Order
--
CREATE TABLE "orders" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "total" decimal NOT NULL, "creation_date" datetime NOT NULL, "departure_date" datetime NOT NULL, "payed" bool NOT NULL, "address_id" bigint NOT NULL REFERENCES "addresses" ("id") DEFERRABLE INITIALLY DEFERRED, "basket_id" bigint NOT NULL UNIQUE REFERENCES "baskets" ("id") DEFERRABLE INITIALLY DEFERRED, "client_id" integer NOT NULL REFERENCES "clients" ("user_id") DEFERRABLE INITIALLY DEFERRED, "delivery_id" bigint NOT NULL REFERENCES "deliveries" ("id") DEFERRABLE INITIALLY DEFERRED, "order_status_id" bigint NOT NULL REFERENCES "statuses" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "orders_staff" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "order_id" bigint NOT NULL REFERENCES "orders" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);

--
-- Add field product to basketproduct
--
CREATE TABLE "new__products_baskets" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "quantity" smallint unsigned NOT NULL CHECK ("quantity" >= 0),
    "basket_id" bigint NOT NULL REFERENCES "baskets" ("id") DEFERRABLE INITIALLY DEFERRED,
    "product_id" bigint NOT NULL REFERENCES "products" ("id") DEFERRABLE INITIALLY DEFERRED
);

INSERT INTO "new__products_baskets"
    ("id", "quantity", "basket_id", "product_id")
SELECT "id", "quantity", "basket_id", NULL
FROM "products_baskets";

DROP TABLE "products_baskets";
ALTER TABLE "new__products_baskets" RENAME TO "products_baskets";

CREATE INDEX "products_category_id_a7a3a156" ON "products" ("category_id");
CREATE INDEX "orders_address_id_38f528bc" ON "orders" ("address_id");
CREATE INDEX "orders_client_id_67f0b211" ON "orders" ("client_id");
CREATE INDEX "orders_delivery_id_4f25da52" ON "orders" ("delivery_id");
CREATE INDEX "orders_order_status_id_05e726df" ON "orders" ("order_status_id");
CREATE UNIQUE INDEX "orders_staff_order_id_user_id_f6659963_uniq" ON "orders_staff" ("order_id", "user_id");
CREATE INDEX "orders_staff_order_id_e381d009" ON "orders_staff" ("order_id");
CREATE INDEX "orders_staff_user_id_27bdc0d6" ON "orders_staff" ("user_id");
CREATE INDEX "products_baskets_basket_id_dd39835a" ON "products_baskets" ("basket_id");
CREATE INDEX "products_baskets_product_id_3e91743f" ON "products_baskets" ("product_id");
COMMIT;
