from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import conf

conf.init()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import auth, admin, demo, course, audit, choice, teacher, faculty, student

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(course.router)
app.include_router(audit.router)
app.include_router(choice.router)
app.include_router(teacher.router)
app.include_router(faculty.router)
app.include_router(student.router)

app.include_router(demo.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host='0.0.0.0', port=28000, reload=True)
