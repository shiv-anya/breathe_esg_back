# Architectural Decisions

### 1. Scope Subsets Handled

- **SAP (Scope 1):** We narrowed this down to a flat-file CSV export representing material movements (specifically movement type 261 - Goods issue for consumption). We chose this because enterprise SAP architectures rarely expose direct OData endpoints to external vendors without months of security clearance.
- **Utility (Scope 2):** Handled as a Portal CSV Export. Utilities rarely have unified APIs. Facilities download monthly spreadsheets with start/end meter dates.
- **Travel (Scope 3):** Handled via a simulated JSON payload modeled closely after the SAP Concur v4 Flight/Trip Itinerary API.

### 2. Flagging Engine Logic

We implemented an automated heuristic engine during ingestion:

- **Negative Values:** Flags rows as `is_flagged = true` and `status = rejected` (as seen in our SAP sample data where reversals or returns create negative amounts, which cannot be blindly calculated as emissions).
- **Unit Mismatches:** If a unit doesn't map to our internal standard conversion tables, it is flagged for manual analyst lookup.

### 3. Questions for the PM

If this weren't a 4-day prototype, I would ask:

1. _For SAP reversals:_ When an amount is negative, is it an accounting correction of a previous month, or a return of fuel to stock? How do we handle matching it to the original entry?
2. _For Utilities:_ How do we split a billing cycle spanning Dec 15 - Jan 15 across calendar reporting years? (Pro-rata split or assignment to end-date?)
