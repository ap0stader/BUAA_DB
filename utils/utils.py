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

def check_semester_name_exist(semester_name: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM semester_table WHERE semester_name=%s", (semester_name,))
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
    cursor.execute('''
        SELECT
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

def get_curriculum_course_id(curriculum_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT curriculum_course_id FROM curriculum_view
        WHERE curriculum_id=%s;
        """, (curriculum_id,))
    return cursor.fetchone()

def get_curriculum_course_type(curriculum_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT course_type FROM curriculum_view
        WHERE curriculum_id=%s;
        """, (curriculum_id,))
    return cursor.fetchone()

def get_curriculum_capacity(curriculum_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT curriculum_capacity FROM curriculum_table
        WHERE curriculum_id=%s;
        """, (curriculum_id,))
    return cursor.fetchone()

def check_is_student_in_curriculum(student_id: str, curriculum_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM attendance_view
        WHERE attendance_student_id=%s AND attendance_curriculum_id=%s;
        """, (student_id, curriculum_id))
    return cursor.fetchone() is not None

def check_choice_curriculum_is_exist(student_id: str, curriculum_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT *
        FROM choice_table 
        WHERE choice_student_id=%s 
            AND choice_curriculum_id=%s
        """, (student_id, curriculum_id))
    return cursor.fetchone() is not None

def check_choice_order_is_exist(student_id: str, curriculum_id: int, order: int):
    course_id = get_curriculum_course_id(curriculum_id)
    course_type = get_curriculum_course_type(curriculum_id)
    conn, cursor = get_cursor('root')
    if course_type in [0, 1]:
        cursor.execute("""
            SELECT
                *
            FROM
                choice_table cht
            JOIN
                curriculum_table ct
            ON
                cht.choice_curriculum_id = ct.curriculum_id
            WHERE
                cht.choice_student_id=%s AND ct.curriculum_course_id=%s AND cht.choice_order=%s;
            """, (student_id, course_id, order))
        return cursor.fetchone() is not None
    else:
        cursor.execute("""
            SELECT
                *
            FROM
                choice_table cht
            JOIN
                curriculum_table ct
            ON
                cht.choice_curriculum_id = ct.curriculum_id
            JOIN
                course_table cot
            ON
                ct.curriculum_course_id = cot.course_id`
            WHERE
                cht.choice_student_id=%s AND cot.course_type=%s AND cht.choice_order=%s;
            """, (student_id, course_type, order))
        return cursor.fetchone() is not None

def check_attendance_curriculum_is_chosen(student_id: str, curriculum_id: str):
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM attendance_view
        WHERE attendance_student_id=%s 
            AND attendance_curriculum_id=%s;
        """, (student_id, curriculum_id))
    return cursor.fetchone() is not None

def check_attendance_course_is_chosen(student_id: str, course_id: str):
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM attendance_view
        WHERE attendance_student_id=%s 
            AND attendance_course_id=%s;
        """, (student_id, course_id))
    return cursor.fetchone() is not None

def get_attendance_curriculum_chosen_count(curriculum_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT COUNT(*) AS count FROM attendance_view
        WHERE attendance_curriculum_id=%s;
        """, (curriculum_id,))
    return cursor.fetchone()

