# Data Model Architecture

Our data model splits the problem into two layers: **Staging/Source Data** (capturing real-world messiness) and **Normalized Activities** (standardized for carbon calculation and auditing).

### Multi-Tenancy & Isolation

Every model inherits from a tenant scoping mechanism to ensure data isolation.

- `Organization`: Represents the client enterprise.
- `Facility/Plant`: Links activities to physical locations (crucial for SAP Plant Codes and Utility Meters).

### Core Schema: `ActivityRecord`

This table represents the normalized internal state before it hits the carbon engine.

| Field             | Type       | Description                                                              |
| :---------------- | :--------- | :----------------------------------------------------------------------- |
| `id`              | UUID / Int | Primary Key.                                                             |
| `organization_id` | ForeignKey | Strict multi-tenancy isolation.                                          |
| `source_type`     | Choice     | `SAP`, `UTILITY`, `TRAVEL`.                                              |
| `raw_payload`     | JSONField  | Stores the exact original row/API response for source-of-truth tracking. |
| `amount`          | Decimal    | Normalized value. Negative values trigger flags.                         |
| `unit`            | String     | Standardized unit (e.g., L, kWh).                                        |
| `scope`           | Choice     | `Scope 1` (Direct/Fuel), `Scope 2` (Electricity), `Scope 3` (Travel).    |
| `status`          | Choice     | `pending`, `approved`, `rejected`.                                       |
| `is_flagged`      | Boolean    | True if failed validation (e.g., negative amount, unknown unit).         |
| `locked`          | Boolean    | Hard lock. Once `True` (Approved), the row is immutable.                 |

### Audit & Lineage Traceability

- **`AuditLog` Table:** Every status transition (`pending` -> `approved`) logs the `user_id`, `timestamp`, and an optional `reason` text field.
- **Immutability:** If `locked` is True, database-level validation (`clean()` or `save()` overrides in Django) blocks updates.
