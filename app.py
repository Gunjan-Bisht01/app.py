from supabase import create_client
import streamlit as st

# Your Supabase credentials
SUPABASE_URL = "https://zpuzelhsplytgkpvnjnh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwdXplbGhzcGx5dGdrcHZuam5oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU5MDk0ODgsImV4cCI6MjA5MTQ4NTQ4OH0.4QgDywkDZbYGEeSf9FlYKTVHRIKMT8nL9tzozRYRsf4"

# Create connection
db = create_client(SUPABASE_URL, SUPABASE_KEY)

# Simple test
st.title("Student Records Project")
st.write("Connection Successful!")

st.title("P1 - Student Records")

# INSERT (run once then comment)
students = [
    {"name": "Ali Hassan", "email": "ali@uni.edu", "age": 20, "gpa": 3.8},
    {"name": "Siti Aishah", "email": "siti@uni.edu", "age": 21, "gpa": 3.2},
    {"name": "Raj Kumar", "email": "raj@uni.edu", "age": 19, "gpa": 2.9},
    {"name": "Lin Wei", "email": "lin@uni.edu", "age": 22, "gpa": 3.5}
]

db.table("students").upsert(students, on_conflict="email").execute()

ids = {r['name']: r['id'] for r in db.table("students").select("id,name").execute().data}

enrollments = [
    {"student_id": ids["Ali Hassan"], "course": "RDBMS", "grade": "A"},
    {"student_id": ids["Ali Hassan"], "course": "Networks", "grade": "B"},
    {"student_id": ids["Siti Aishah"], "course": "RDBMS", "grade": "B"},
    {"student_id": ids["Raj Kumar"], "course": "RDBMS", "grade": "C"},
    {"student_id": ids["Lin Wei"], "course": "Networks", "grade": "A"}
]
#db.table("students").insert(students).execute()
db.table("enrollments").insert(enrollments).execute()

# SELECT
st.subheader("All Students")
st.dataframe(db.table("students").select("*").execute().data)

# WHERE
st.subheader("GPA >= 3.5")
st.dataframe(db.table("students").select("name,gpa").gte("gpa", 3.5).execute().data)

# JOIN
st.subheader("RDBMS Enrollments")
st.dataframe(
    db.table("enrollments")
    .select("grade, students(name)")
    .eq("course", "RDBMS")
    .execute().data
)

# UPDATE
db.table("students").update({"gpa": 3.9}).eq("name", "Ali Hassan").execute()

st.write("Updated Ali:")
st.dataframe(db.table("students").select("name,gpa").eq("name", "Ali Hassan").execute().data)