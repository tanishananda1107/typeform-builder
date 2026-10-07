import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base,engine
from .routers.forms import router as forms_router
from .routers.responses import router as responses_router
from .seed import seed
Base.metadata.create_all(bind=engine);seed()
app=FastAPI(title='Formly Typeform Builder API',version='2.0.0')
origins=[x.strip() for x in os.getenv('CORS_ORIGINS','http://localhost:3000').split(',') if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(forms_router);app.include_router(responses_router)
@app.get('/api/health')
def health():return {'status':'ok','service':'formly-api'}
