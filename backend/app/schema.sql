CREATE TABLE IF NOT EXISTS slots (
    building VARCHAR (10),
    slot INT,
    status NUMBER(1),
    CONSTRAINT status_bool CHECK (status IN (1,0)),
    PRIMARY KEY (building, slot)
);