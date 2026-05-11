# Normalization Report — 3rd Normal Form Audit

## Original Schema

```
Patients(patient_id, name, date_of_birth, metadata_created_by)
Doctors(doctor_id, name, specialization, metadata_source)
Admissions(admission_id, patient_id, doctor_id, admission_date, discharge_date, metadata_notes, stay_length)
```

---

## 1. Original Functional Dependencies

**Patients:**
- `patient_id → name, date_of_birth, metadata_created_by`

**Doctors:**
- `doctor_id → name, specialization, metadata_source`

**Admissions:**
- `admission_id → patient_id, doctor_id, admission_date, discharge_date, metadata_notes`
- `admission_id → stay_length` *(derived: discharge_date − admission_date)*

---

## 2. Anomaly Identification

### Update Anomaly
- If a doctor's specialization changes, only one row needs updating — no risk here since specialization is in its own table. ✅

### Insertion Anomaly
- A doctor cannot be recorded without at least one admission if they are only in Admissions. Since Doctors is its own table, this is fine. ✅

### Deletion Anomaly
- Deleting the last admission for a patient would not delete the patient record. ✅

### Transitive Dependency (3NF Violation)
- **`stay_length`** in Admissions is functionally determined by `discharge_date` and `admission_date`, both of which are non-key attributes.  
  `admission_id → discharge_date → stay_length` — this is a **transitive dependency**, violating 3NF.
- **`metadata_*`** columns (`metadata_created_by`, `metadata_source`, `metadata_notes`) carry operational tracking data with no functional relevance to the entity's identity. These are removed to keep the schema clean.

---

## 3. Decomposition Steps

### Step 1 — Remove `stay_length` (transitive dependency)
`stay_length` is derived from `discharge_date − admission_date`. Storing it creates redundancy and risks inconsistency.

**Fix:** Drop the column. Compute it at query time:
```sql
SELECT DATEDIFF(discharge_date, admission_date) AS stay_length FROM Admissions;
```
In Python, it is exposed as a `@property` on the `Admission` model — never written to the database.

### Step 2 — Remove `metadata_*` columns
These columns are operational metadata with no business-logic dependencies and no place in a normalized relational schema.

---

## 4. Final Relational Schema (3NF)

```
Patients(patient_id PK, name UNIQUE NOT NULL, date_of_birth NOT NULL)

Doctors(doctor_id PK, name NOT NULL, specialization NOT NULL)

Admissions(admission_id PK,
           patient_id FK → Patients,
           doctor_id  FK → Doctors,
           admission_date NOT NULL,
           discharge_date,
           notes)
```

### Verification Against Normal Forms

| Normal Form | Check | Status |
|-------------|-------|--------|
| 1NF | All values atomic, every row unique, primary keys defined | ✅ |
| 2NF | No partial dependencies (all PKs are single-column) | ✅ |
| 3NF | No transitive dependencies (`stay_length` removed) | ✅ |
