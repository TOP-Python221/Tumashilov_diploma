BEGIN;
--
-- Alter field discount on product
--
CREATE TABLE "new__products" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "discount" smallint unsigned NULL CHECK ("discount" >= 0),
    "name" varchar(255) NOT NULL,
    "price" decimal NOT NULL,
    "availability" smallint unsigned NOT NULL CHECK ("availability" >= 0),
    "image" varchar(100) NULL,
    "category_id" bigint NOT NULL REFERENCES "categories" ("id") DEFERRABLE INITIALLY DEFERRED
);

INSERT INTO "new__products"
    ("id", "name", "price", "availability", "image", "category_id", "discount")
SELECT
    "id", "name", "price", "availability", "image", "category_id", "discount"
FROM "products";

DROP TABLE "products";
ALTER TABLE "new__products" RENAME TO "products";
CREATE INDEX "products_category_id_a7a3a156" ON "products" ("category_id");

COMMIT;
