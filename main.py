from fastapi import FastAPI
import conf

conf.init()

app = FastAPI()

from routers import auth, admin, demo, course, audit, choise, teacher, faculty, student

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(course.router)
app.include_router(audit.router)
app.include_router(choise.router)
app.include_router(teacher.router)
app.include_router(faculty.router)
app.include_router(student.router)

app.include_router(demo.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host='0.0.0.0', port=28000, reload=True)
