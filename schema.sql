CREATE TABLE measurement_type(
    id INT NOT NULL,
    type TEXT NOT NULL,
    units TEXT,
    PRIMARY KEY (id)
);

INSERT INTO measurement_type values(1, "Temperature", "Celsius");
INSERT INTO measurement_type values(2, "Humidity", "%");
INSERT INTO measurement_type values(3, "Pressure", "mPa");
INSERT INTO measurement_type values(4, "CO2", "ppm");


CREATE TABLE measurement (
    id INT NOT NULL AUTO_INCREMENT,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    mtype INT NOT NULL,
    data FLOAT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (mtype) REFERENCES measurement_type (id)
);
