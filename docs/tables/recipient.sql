CREATE TABLE CustomerMap(
    id                      INT             PRIMARY KEY,
    wcid                    INT             NOT NULL        UNIQUE,
    last_update             DATETIME        NOT NULL,
    update_required         BIT             NOT NULL        DEFAULT 0
)


CREATE TABLE CategoryMap(
    id                      INT             PRIMARY KEY,
    wcid                    INT             NOT NULL        UNIQUE,
    last_update             DATETIME        NOT NULL,
    update_required         BIT             NOT NULL        DEFAULT 0
)


CREATE TABLE ProductMap(
    id                      INT             PRIMARY KEY,
    wcid                    INT             NOT NULL        UNIQUE,
    last_update             DATETIME        NOT NULL,
    update_required         BIT             NOT NULL        DEFAULT 0
)


CREATE TABLE InvoiceMap(
    id                      INT             PRIMARY KEY,
    wcid                    INT             NOT NULL        UNIQUE,
    last_update             DATETIME        NOT NULL,
    update_required         BIT             NOT NULL        DEFAULT 0
)
