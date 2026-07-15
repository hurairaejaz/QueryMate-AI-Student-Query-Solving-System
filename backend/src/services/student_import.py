import pandas as pd
from sqlalchemy.orm import Session
from src.models.student_record import StudentRecord


def import_students(db: Session):
    file_path = r"F:\Querymate\backend\uploads\kb_files\View Student Details.xlsx"

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise Exception(f"Failed to read Excel file: {str(e)}")

    #  Validate required columns
    required_columns = ["Roll No.", "Name / Father Name"]

    for col in required_columns:
        if col not in df.columns:
            raise Exception(f"Missing column in Excel: {col}")

    #  Remove duplicates
    df = df.drop_duplicates(subset=["Roll No."])

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        roll_number = str(row["Roll No."]).strip()
        name = str(row["Name / Father Name"]).strip()

        # skip empty rows
        if not roll_number or roll_number.lower() == "nan":
            continue

        #  check if already exists
        existing = db.query(StudentRecord).filter(
            StudentRecord.roll_number == roll_number
        ).first()

        if existing:
            skipped += 1
            continue

        student = StudentRecord(
            roll_number=roll_number,
            name=name
        )

        db.add(student)
        inserted += 1

    db.commit()

    return {
        "message": "Import completed",
        "inserted": inserted,
        "skipped_duplicates": skipped
    }