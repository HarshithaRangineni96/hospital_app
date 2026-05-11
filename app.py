"""
Hospital Admissions App — Flask + SQLAlchemy
Run:  python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import date

app = Flask(__name__)
app.secret_key = "hospital_secret_key_change_in_prod"

# ── Database Config ──────────────────────────────────────────
# Change user/password/host/dbname to match your MySQL setup
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:password@localhost/hospital_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ── Models ───────────────────────────────────────────────────

class Patient(db.Model):
    __tablename__ = "Patients"
    patient_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name          = db.Column(db.String(100), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    admissions    = db.relationship("Admission", backref="patient",
                                    cascade="all, delete-orphan", lazy=True)


class Doctor(db.Model):
    __tablename__ = "Doctors"
    doctor_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name           = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    admissions     = db.relationship("Admission", backref="doctor",
                                     cascade="all, delete-orphan", lazy=True)


class Admission(db.Model):
    __tablename__  = "Admissions"
    admission_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id     = db.Column(db.Integer, db.ForeignKey("Patients.patient_id"), nullable=False)
    doctor_id      = db.Column(db.Integer, db.ForeignKey("Doctors.doctor_id"),  nullable=False)
    admission_date = db.Column(db.Date, nullable=False)
    discharge_date = db.Column(db.Date, nullable=True)
    notes          = db.Column(db.String(100), nullable=True)

    @property
    def stay_length(self):
        """Computed — never stored (3NF compliance)."""
        if self.discharge_date and self.admission_date:
            return (self.discharge_date - self.admission_date).days
        return None


# ── Dashboard ────────────────────────────────────────────────

@app.route("/")
def dashboard():
    total_patients   = Patient.query.count()
    total_doctors    = Doctor.query.count()
    total_admissions = Admission.query.count()
    active_admissions = Admission.query.filter(Admission.discharge_date == None).count()  # noqa

    avg_stay = db.session.execute(text(
        "SELECT AVG(DATEDIFF(discharge_date, admission_date)) "
        "FROM Admissions WHERE discharge_date IS NOT NULL"
    )).scalar()

    top_doctor = db.session.execute(text(
        "SELECT d.name, COUNT(a.admission_id) AS cnt "
        "FROM Doctors d JOIN Admissions a ON d.doctor_id = a.doctor_id "
        "GROUP BY d.name ORDER BY cnt DESC LIMIT 1"
    )).fetchone()

    admissions_by_year = db.session.execute(text(
        "SELECT YEAR(admission_date) AS yr, COUNT(*) AS cnt "
        "FROM Admissions GROUP BY yr ORDER BY yr"
    )).fetchall()

    return render_template(
        "dashboard.html",
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_admissions=total_admissions,
        active_admissions=active_admissions,
        avg_stay=round(float(avg_stay), 1) if avg_stay else 0,
        top_doctor=top_doctor,
        admissions_by_year=admissions_by_year,
    )


# ── Patients ─────────────────────────────────────────────────

@app.route("/patients")
def patients():
    all_patients = Patient.query.order_by(Patient.name).all()
    return render_template("patients.html", patients=all_patients)


@app.route("/patients/add", methods=["POST"])
def add_patient():
    name = request.form.get("name", "").strip()
    dob  = request.form.get("date_of_birth", "").strip()

    if not name or not dob:
        flash("Name and date of birth are required.", "danger")
        return redirect(url_for("patients"))

    if Patient.query.filter_by(name=name).first():
        flash("A patient with that name already exists.", "danger")
        return redirect(url_for("patients"))

    db.session.add(Patient(name=name, date_of_birth=dob))
    db.session.commit()
    flash(f"Patient '{name}' added successfully.", "success")
    return redirect(url_for("patients"))


@app.route("/patients/delete/<int:pid>", methods=["POST"])
def delete_patient(pid):
    """Transaction: cascades delete to admissions first."""
    try:
        patient = Patient.query.get_or_404(pid)
        db.session.delete(patient)   # cascade handles Admissions
        db.session.commit()
        flash("Patient and related admissions deleted.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Delete failed: {exc}", "danger")
    return redirect(url_for("patients"))


@app.route("/patients/edit/<int:pid>", methods=["POST"])
def edit_patient(pid):
    """Update a patient's name and/or date of birth."""
    patient = Patient.query.get_or_404(pid)
    name = request.form.get("name", "").strip()
    dob  = request.form.get("date_of_birth", "").strip()

    if not name or not dob:
        flash("Name and date of birth are required.", "danger")
        return redirect(url_for("patients"))

    existing = Patient.query.filter_by(name=name).first()
    if existing and existing.patient_id != pid:
        flash("Another patient with that name already exists.", "danger")
        return redirect(url_for("patients"))

    try:
        patient.name = name
        patient.date_of_birth = dob
        db.session.commit()
        flash(f"Patient '{name}' updated successfully.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Update failed: {exc}", "danger")
    return redirect(url_for("patients"))


# ── Doctors ──────────────────────────────────────────────────

@app.route("/doctors")
def doctors():
    all_doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template("doctors.html", doctors=all_doctors)


@app.route("/doctors/add", methods=["POST"])
def add_doctor():
    name = request.form.get("name", "").strip()
    spec = request.form.get("specialization", "").strip()

    if not name or not spec:
        flash("Name and specialization are required.", "danger")
        return redirect(url_for("doctors"))

    db.session.add(Doctor(name=name, specialization=spec))
    db.session.commit()
    flash(f"Doctor '{name}' added.", "success")
    return redirect(url_for("doctors"))


@app.route("/doctors/delete/<int:did>", methods=["POST"])
def delete_doctor(did):
    try:
        doctor = Doctor.query.get_or_404(did)
        db.session.delete(doctor)
        db.session.commit()
        flash("Doctor and related admissions deleted.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Delete failed: {exc}", "danger")
    return redirect(url_for("doctors"))


@app.route("/doctors/edit/<int:did>", methods=["POST"])
def edit_doctor(did):
    """Update a doctor's name and/or specialization."""
    doctor = Doctor.query.get_or_404(did)
    name = request.form.get("name", "").strip()
    spec = request.form.get("specialization", "").strip()

    if not name or not spec:
        flash("Name and specialization are required.", "danger")
        return redirect(url_for("doctors"))

    try:
        doctor.name = name
        doctor.specialization = spec
        db.session.commit()
        flash(f"Doctor '{name}' updated successfully.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Update failed: {exc}", "danger")
    return redirect(url_for("doctors"))


# ── Admissions ───────────────────────────────────────────────

@app.route("/admissions")
def admissions():
    all_admissions = (
        Admission.query
        .order_by(Admission.admission_date.desc())
        .all()
    )
    patients = Patient.query.order_by(Patient.name).all()
    doctors  = Doctor.query.order_by(Doctor.name).all()
    return render_template(
        "admissions.html",
        admissions=all_admissions,
        patients=patients,
        doctors=doctors,
    )


@app.route("/admissions/add", methods=["POST"])
def add_admission():
    pid      = request.form.get("patient_id")
    did      = request.form.get("doctor_id")
    adm_date = request.form.get("admission_date", "").strip()
    dis_date = request.form.get("discharge_date", "").strip() or None
    notes    = request.form.get("notes", "").strip()

    if not pid or not did or not adm_date:
        flash("Patient, doctor, and admission date are required.", "danger")
        return redirect(url_for("admissions"))

    db.session.add(Admission(
        patient_id=pid, doctor_id=did,
        admission_date=adm_date, discharge_date=dis_date,
        notes=notes or None,
    ))
    db.session.commit()
    flash("Admission recorded.", "success")
    return redirect(url_for("admissions"))


@app.route("/admissions/discharge/<int:aid>", methods=["POST"])
def discharge_patient(aid):
    """Transaction: mark today as discharge date."""
    adm = Admission.query.get_or_404(aid)
    if adm.discharge_date:
        flash("Patient is already discharged.", "warning")
    else:
        adm.discharge_date = date.today()
        db.session.commit()
        flash("Patient discharged today.", "success")
    return redirect(url_for("admissions"))


@app.route("/admissions/delete/<int:aid>", methods=["POST"])
def delete_admission(aid):
    Admission.query.filter_by(admission_id=aid).delete()
    db.session.commit()
    flash("Admission record deleted.", "success")
    return redirect(url_for("admissions"))


@app.route("/admissions/edit/<int:aid>", methods=["POST"])
def edit_admission(aid):
    """Update admission dates and notes."""
    adm = Admission.query.get_or_404(aid)
    pid      = request.form.get("patient_id")
    did      = request.form.get("doctor_id")
    adm_date = request.form.get("admission_date", "").strip()
    dis_date = request.form.get("discharge_date", "").strip() or None
    notes    = request.form.get("notes", "").strip() or None

    if not pid or not did or not adm_date:
        flash("Patient, doctor, and admission date are required.", "danger")
        return redirect(url_for("admissions"))

    if dis_date and dis_date < adm_date:
        flash("Discharge date cannot be before admission date.", "danger")
        return redirect(url_for("admissions"))

    try:
        adm.patient_id     = pid
        adm.doctor_id      = did
        adm.admission_date = adm_date
        adm.discharge_date = dis_date
        adm.notes          = notes
        db.session.commit()
        flash("Admission updated successfully.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Update failed: {exc}", "danger")
    return redirect(url_for("admissions"))


# ── Run ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
