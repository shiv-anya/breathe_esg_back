# Real-World Source Research

### 1. SAP Fuel & Procurement

- **Research:** Real SAP implementations frequently output flat records where column headers are abbreviated German technical terms (e.g., `MENGE` for Quantity, `MEINS` for Unit, `MATNR` for Material Number).
- **Why our sample looks this way:** Our mock data includes entries with negative numbers (`"amount": -100.0`). This is realistic; SAP uses negative lines or specific movement types to indicate accounting reversals, cancellations, or inventory corrections.
- **What breaks in production:** Custom SAP configurations where a plant code changes meaning between different corporate entities.

### 2. Utility Portals (Electricity)

- **Research:** Utility data exports (like PG&E or National Grid portal downloads) rarely align with neat calendar months. They contain `Bill_Start_Date` and `Bill_End_Date` rows, alongside total consumption in kWh.
- **Why our sample looks this way:** The dates naturally overlap calendar boundaries, forcing the application layer to recognize that a single row might span two different reporting quarters.
- **What breaks in production:** Estimated bills. Utilities often publish an "Estimated" read and then correct it 3 months later with an "Actual" read, creating duplicate, conflicting data for the same period.

### 3. Corporate Travel (Concur/Navan)

- **Research:** Concur's Travel Profile and Itinerary APIs output complex nested JSON arrays. They frequently lack explicit mileage distances, providing only IATA airport codes (e.g., `JFK`, `LHR`) and cabin class (`Economy`, `Business`).
- **Why our sample looks this way:** Data records are structured by trip segment rather than total distance, requiring a lookup table of airport coordinates to map distances accurately.
- **What breaks in production:** Multi-leg flights where a traveler misses a connection, leading to a discrepancy between booked itineraries and actual miles flown.
