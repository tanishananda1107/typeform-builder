import json,re,secrets
from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Creator,Form,Question
from ..schemas import FormCreate,FormUpdate,QuestionCreate,QuestionUpdate,Reorder
router=APIRouter(prefix='/api',tags=['forms']);ALLOWED={'short_text','long_text','multiple_choice','dropdown','email','number','yes_no','rating'}
def slugify(s):
 base=re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-') or 'form';return f'{base}-{secrets.token_hex(2)}'
def j(s):
 try:return json.loads(s or '{}')
 except:return {}
def serialize_question(q):return {'id':q.id,'position':q.position,'type':q.type,'title':q.title,'description':q.description or '','required':q.required,'settings':j(q.settings_json)}
def serialize_form(f):return {'id':f.id,'title':f.title,'slug':f.slug,'description':f.description or '','status':f.status,'response_count':len(f.responses),'questions':[serialize_question(q) for q in f.questions],'theme':j(f.theme_json),'thank_you':j(f.thank_you_json)}
@router.get('/forms')
def list_forms(db:Session=Depends(get_db)):return [serialize_form(f) for f in db.query(Form).order_by(Form.updated_at.desc()).all()]
@router.post('/forms')
def create_form(data:FormCreate,db:Session=Depends(get_db)):
 c=db.query(Creator).first()
 if not c:c=Creator(name='Demo Creator',email='demo@example.com');db.add(c);db.flush()
 f=Form(creator_id=c.id,title=data.title.strip() or 'Untitled form',slug=slugify(data.title),status='draft');db.add(f);db.commit();db.refresh(f);return serialize_form(f)
@router.get('/forms/{form_id}')
def get_form(form_id:int,db:Session=Depends(get_db)):
 f=db.get(Form,form_id)
 if not f:raise HTTPException(404,'Form not found')
 return serialize_form(f)
@router.patch('/forms/{form_id}')
def update_form(form_id:int,data:FormUpdate,db:Session=Depends(get_db)):
 f=db.get(Form,form_id)
 if not f:raise HTTPException(404,'Form not found')
 if data.title is not None:f.title=data.title.strip() or f.title
 if data.description is not None:f.description=data.description
 if data.theme is not None:f.theme_json=json.dumps(data.theme)
 if data.thank_you is not None:f.thank_you_json=json.dumps(data.thank_you)
 db.commit();db.refresh(f);return serialize_form(f)
@router.delete('/forms/{form_id}')
def delete_form(form_id:int,db:Session=Depends(get_db)):
 f=db.get(Form,form_id)
 if not f:raise HTTPException(404,'Form not found')
 db.delete(f);db.commit();return {'ok':True}
@router.post('/forms/{form_id}/duplicate')
def duplicate_form(form_id:int,db:Session=Depends(get_db)):
 src=db.get(Form,form_id)
 if not src:raise HTTPException(404,'Form not found')
 f=Form(creator_id=src.creator_id,title=f'{src.title} copy',slug=slugify(src.title),description=src.description,status='draft',theme_json=src.theme_json,thank_you_json=src.thank_you_json);db.add(f);db.flush()
 for q in src.questions:db.add(Question(form_id=f.id,position=q.position,type=q.type,title=q.title,description=q.description,required=q.required,settings_json=q.settings_json))
 db.commit();db.refresh(f);return serialize_form(f)
@router.post('/forms/{form_id}/publish')
def publish(form_id:int,db:Session=Depends(get_db)):
 f=db.get(Form,form_id)
 if not f:raise HTTPException(404,'Form not found')
 if not f.questions:raise HTTPException(400,'Add at least one question before publishing')
 f.status='published';f.published_at=datetime.utcnow();db.commit();return {'status':'published','slug':f.slug}
@router.post('/forms/{form_id}/unpublish')
def unpublish(form_id:int,db:Session=Depends(get_db)):
 f=db.get(Form,form_id)
 if not f:raise HTTPException(404,'Form not found')
 f.status='draft';f.published_at=None;db.commit();return {'status':'draft'}
@router.post('/forms/{form_id}/questions')
def add_question(form_id:int,data:QuestionCreate,db:Session=Depends(get_db)):
 f=db.get(Form,form_id)
 if not f:raise HTTPException(404,'Form not found')
 if data.type not in ALLOWED:raise HTTPException(400,'Unsupported question type')
 q=Question(form_id=form_id,position=len(f.questions),type=data.type,title=data.title,description=data.description,required=data.required,settings_json=json.dumps(data.settings));db.add(q);db.commit();db.refresh(q);return serialize_question(q)
@router.patch('/questions/{question_id}')
def update_question(question_id:int,data:QuestionUpdate,db:Session=Depends(get_db)):
 q=db.get(Question,question_id)
 if not q:raise HTTPException(404,'Question not found')
 if data.type is not None:
  if data.type not in ALLOWED:raise HTTPException(400,'Unsupported question type')
  q.type=data.type
 if data.title is not None:q.title=data.title
 if data.description is not None:q.description=data.description
 if data.required is not None:q.required=data.required
 if data.settings is not None:q.settings_json=json.dumps(data.settings)
 db.commit();db.refresh(q);return serialize_question(q)
@router.delete('/questions/{question_id}')
def delete_question(question_id:int,db:Session=Depends(get_db)):
 q=db.get(Question,question_id)
 if not q:raise HTTPException(404,'Question not found')
 form=q.form;db.delete(q);db.flush()
 for i,item in enumerate(form.questions):item.position=i
 db.commit();return {'ok':True}
@router.patch('/forms/{form_id}/questions/reorder')
def reorder(form_id:int,data:Reorder,db:Session=Depends(get_db)):
 f=db.get(Form,form_id)
 if not f:raise HTTPException(404,'Form not found')
 qs={q.id:q for q in f.questions}
 if set(qs)!=set(data.question_ids):raise HTTPException(400,'Question list does not match form')
 for i,qid in enumerate(data.question_ids):qs[qid].position=i
 db.commit();return {'ok':True}
