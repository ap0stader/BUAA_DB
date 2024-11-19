from fastapi import FastAPI
import conf

conf.init()

app = FastAPI()

from routers import auth, admin

app.include_router(auth.router)
app.include_router(admin.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host='0.0.0.0', port=28000, reload=True)
