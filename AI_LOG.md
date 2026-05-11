# AI Usage Log

This file documents every instance of Generative AI assistance used during the development of this project, as required by the course AI policy.

---

## Entry 1

- **Tool:** Claude (Anthropic — claude.ai)
- **Prompt:** "My professor gave me this SQL schema for a hospital database (Patients, Doctors, Admissions). Help me build a full-stack Flask app for Project 3 including CRUD, transactions, validation, and a summary dashboard."
- **AI Output:** Generated `app.py` with Flask routes for all three tables, SQLAlchemy models, dashboard aggregate queries, and Jinja2 HTML templates with Bootstrap styling.
- **My Modifications:**
  - Updated the `SQLALCHEMY_DATABASE_URI` to match my local MySQL credentials
  - Verified that the cascade delete behavior matched our foreign key constraints from the original schema
  - Adjusted the dashboard queries to use the correct table and column names from my schema
  - Reviewed all server-side validation logic to ensure it matched the project requirements

---

## Entry 2

- **Tool:** Claude (Anthropic — claude.ai)
- **Prompt:** "Help me write the NORMALIZATION.md documenting my 3NF audit for this hospital schema."
- **AI Output:** Identified the `stay_length` transitive dependency and `metadata_*` fields as normalization issues. Generated decomposition steps and the final 3NF schema.
- **My Modifications:**
  - Confirmed the transitive dependency analysis against my lecture notes on 3NF
  - Verified the final schema matches what is actually implemented in `schema.sql` and `app.py`

---

*Add additional entries below for any further AI assistance used.*

---

## Entry 3

- **Tool:** Claude (Anthropic — claude.ai)
- **Prompt:** "Help me add Edit/Update functionality for Patients, Doctors, and Admissions so the app has full CRUD."
- **AI Output:** Generated three new Flask routes (`/patients/edit/<id>`, `/doctors/edit/<id>`, `/admissions/edit/<id>`) with server-side validation, and added Bootstrap modal forms with pre-filled values to each corresponding HTML template.
- **My Modifications:**
  - Verified that the modal `action` URLs matched the new Flask route paths
  - Confirmed that pre-filled `value` attributes in the edit forms correctly reference the SQLAlchemy model fields
  - Checked that the discharge-date validation logic (discharge cannot precede admission) matched business requirements
