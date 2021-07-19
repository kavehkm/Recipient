CREATE TABLE Customer(
    id                  INT                 PRIMARY KEY           IDENTITY,
    firstname           NVARCHAR(50)        NOT NULL,
    lastname            NVARCHAR(50)        NOT NULL
)


CREATE TABLE Category(
    id                  INT                 PRIMARY KEY           IDENTITY,
    name                NVARCHAR(100)       NOT NULL              UNIQUE
)


CREATE TABLE Product(
    id                  INT                 PRIMARY KEY           IDENTITY,
    name                NVARCHAR(100)       NOT NULL,
    price               FLOAT               NOT NULL,
    category_id         INT                 NOT NULL
)


CREATE TABLE Invoice(
    id                  INT                 PRIMARY KEY           IDENTITY,
    customer_id         INT                 NOT NULL,
    created_date        DATETIME            NOT NULL
)


CREATE TABLE ItemLine(
    invoice_id          INT                 NOT NULL,
    product_id          INT                 NOT NULL,
    quantity            INT                 NOT NULL
)
