from fastapi import FastAPI, Request
from database import engine, Base
from routers import auth, profile, bookings, venues, courts, coupons
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import SQLALCHEMY_DATABASE_URL
from fastapi.responses import JSONResponse
import traceback

# Lifespan event to create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        if "sqlite" in SQLALCHEMY_DATABASE_URL:
            db_type = "SQLite"
        elif "postgresql" in SQLALCHEMY_DATABASE_URL:
            db_type = "PostgreSQL"
        else:
            db_type = "MySQL"
            
        print(f"[DB] Connecting to database: {db_type}")
        
        # Base.metadata.create_all(bind=engine)
        print("[DB] Database tables created successfully")
    except Exception as e:
        print(f"[DB WARN] Database connection failed: {e}")
        print("[DB WARN] Server starting but database connection failed. Check your .env configuration.")
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan, debug=True)

# CORS Configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[ERROR] Global exception handler: {type(exc).__name__}: {str(exc)}", flush=True)
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}", "type": type(exc).__name__}
    )

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(bookings.router)
app.include_router(venues.router)
app.include_router(courts.router)
app.include_router(coupons.router, prefix="/coupons", tags=["coupons"])

@app.get("/")
def read_root():
    return {"message": "Welcome to MyRush API"}
