import os
from pathlib import Path
from utils.db import get_cursor


UPLOAD_DIR = Path("/home/webmaster/static/upload")
UPLOAD_DIR.mkdir(exist_ok=True)


def check_place_id_exist(place_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM place_table WHERE place_id=%s", (place_id,))
    return cursor.fetchone() is not None

def check_place_name_exist(place_name: str, ex_place_id: int = -1):
    conn, cursor = get_cursor('root')
    if ex_place_id == -1:
        cursor.execute("SELECT * FROM place_table WHERE place_name=%s", (place_name,))
    else:
        cursor.execute("SELECT * FROM place_table WHERE place_name=%s AND place_id!=%s", (place_name, ex_place_id))
    return cursor.fetchone() is not None

def check_department_id_exist(department_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM department_table WHERE department_id=%s", (department_id,))
    return cursor.fetchone() is not None

def check_department_name_exist(department_name: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM department_table WHERE department_name=%s", (department_name,))
    return cursor.fetchone() is not None

def check_major_id_exist(major_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM major_table WHERE major_id=%s", (major_id,))
    return cursor.fetchone() is not None

def check_major_name_exist(major_name: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM major_table WHERE major_name=%s", (major_name,))
    return cursor.fetchone() is not None

def check_class_id_exist(class_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM class_table WHERE class_id=%s", (class_id,))
    return cursor.fetchone() is not None

def check_teacher_is_master(teacher_id: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM class_table WHERE class_teacher_id=%s", (teacher_id,))
    return cursor.fetchone() is not None

def check_teacher_id_exist(teacher_id: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM teacher_table WHERE teacher_id=%s", (teacher_id,))
    return cursor.fetchone() is not None

def check_login_id_exist(id: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM login_table WHERE login_id=%s", (id,))
    return cursor.fetchone() is not None

def check_student_id_exist(student_id: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM student_table WHERE student_id=%s", (student_id,))
    return cursor.fetchone() is not None

def check_faculty_id_exist(faculty_id: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM faculty_table WHERE faculty_id=%s", (faculty_id,))
    return cursor.fetchone() is not None

def check_course_id_exist(course_id: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM course_table WHERE course_id=%s", (course_id,))
    return cursor.fetchone() is not None

def check_semester_id_exist(semester_id: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM semester_table WHERE semester_id=%s", (semester_id,))
    return cursor.fetchone() is not None

def check_curriculum_id_exist(curriculum_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM curriculum_table WHERE curriculum_id=%s", (curriculum_id,))
    return cursor.fetchone() is not None

def get_curriculum(curriculum_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM curriculum_table WHERE curriculum_id=%s", (curriculum_id,))
    return cursor.fetchone()

def get_place_table():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM place_table")
    table = {}
    for row in cursor.fetchall():
        table[row['place_id']] = row['place_name']
        table[row['place_name']] = row['place_id']
    return table

def get_curriculums_resource(semester_id: int, ex_curriculum_id: int = -1):
    conn, cursor = get_cursor('root')
    cursor.execute(
'''SELECT 
    cust.curriculum_utilization_string AS resource
FROM 
    curriculum_table ct
JOIN 
    curriculum_utilization_string_table cust
ON 
    ct.curriculum_id = cust.curriculum_id
WHERE 
    ct.curriculum_semester_id=%s AND ct.curriculum_id!=%s;
''', (semester_id, ex_curriculum_id))
    resources = []
    for row in cursor.fetchall():
        resources.append(row['resource'])
    return resources
