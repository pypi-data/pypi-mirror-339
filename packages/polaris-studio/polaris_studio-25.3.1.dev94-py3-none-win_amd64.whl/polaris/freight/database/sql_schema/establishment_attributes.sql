-- Copyright (c) 2025, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ An output table for the establishments
--@ and their assets, including: heavy and medium duty trucks,
--@ and carriers

CREATE TABLE Establishment_Attribute (
    "establishment"              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, --@ The establishment identifier
    "location"                   INTEGER NOT NULL DEFAULT 0, --@ The selected location of the establishment (foreign key to the Location table)
    "medium_duty_trucks"         INTEGER NOT NULL DEFAULT 0, --@ Number of medium duty trucks owned by the establishment
    "heavy_duty_trucks"          INTEGER NOT NULL DEFAULT 0, --@ Number of heavy duty trucks owned by the establishment
    "carrier_establishment"      INTEGER NOT NULL DEFAULT 0, --@ Carrier establishment identifier (foreign key to the Establishment table)

    CONSTRAINT establishment_fk FOREIGN KEY (establishment)
    REFERENCES Establishment (establishment) DEFERRABLE INITIALLY DEFERRED

);
