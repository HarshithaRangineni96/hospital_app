# AI Usage Log

This file documents every instance of Generative AI assistance used during the development of this project, as required by the course AI policy.

---

## Entry 1

- **Tool:** Claude (Anthropic — claude.ai)
- **Prompt:** "I already created my hospital database application. I am only asking for learning guidance and understanding about how the application structure, validation, dashboard queries, Flask routes, and frontend organization work so I can improve and modify my own project myself."
- **AI Output:** Provided learning guidance and reference explanations related to Flask application structure, validation handling, dashboard queries, and frontend organization.
- **My Modifications:**
  - Understood the concepts and modified the implementation based on my own schema and project requirements
  - Verified the application functionality and validation logic myself


---

## Entry 2

- **Tool:** Claude (Anthropic — claude.ai)
- **Prompt:** "Help me write the NORMALIZATION.md documenting my 3NF audit for this hospital schema."
- **AI Output:** Provided explanations and reference guidance related to normalization concepts, transitive dependencies, and 3NF documentation.
- **My Modifications:**
  - Verified the normalization concepts using lecture notes and my own schema
  - Updated the documentation according to my implemented database design

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
