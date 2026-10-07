import json,re
from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Form,Response,Answer
from ..schemas import ResponseCreate
router=APIRouter(prefix='/api',tags=['responses'])
def public_question(q):return {'id':q.id,'position':q.position,'type':q.type,'title':q.title,'description':q.description or '','required':q.required,'settings':json.loads(q.settings_json or '{}')}
def value_for_answer(a):
 if a.value_text is not None:return a.value_text
 if a.value_number is not None:
  try:return float(a.value_number) if '.' in a.value_number else int(a.value_number)
  except:return a.value_number
 if a.value_boolean is not None:return a.value_boolean
 if a.value_json is not None:
  try:return json.loads(a.value_json)
  except:return a.value_json
 return None
def validate(q,value):
 settings=json.loads(q.settings_json or '{}')
 if q.required and (value is None or value==''):raise HTTPException(422,f"'{q.title}' is required")
 if value in (None,''):return
 if q.type=='email' and not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$',str(value)):raise HTTPException(422,f"Invalid email for '{q.title}'")
 if q.type=='number':
  try:float(value)
  except:raise HTTPException(422,f"Invalid number for '{q.title}'")
 if q.type in ('multiple_choice','dropdown') and str(value) not in [str(x) for x in settings.get('options',[])]:raise HTTPException(422,f"Invalid option for '{q.title}'")
 if q.type=='yes_no' and str(value) not in ('Yes','No'):raise HTTPException(422,f"Invalid answer for '{q.title}'")
 if q.type=='rating':
  try:
   n=float(value);lo=float(settings.get('min',1));hi=float(settings.get('max',5))
   if not lo<=n<=hi:raise ValueError
  except:raise HTTPException(422,f"Invalid rating for '{q.title}'")
@router.get('/public/forms/{slug}')
def public_form(slug:str,db:Session=Depends(get_db)):
 f=db.query(Form).filter(Form.slug==slug,Form.status=='published').first()
 if not f:raise HTTPException(404,'Published form not found')
 return {'id':f.id,'title':f.title,'description':f.description or '','slug':f.slug,'theme':json.loads(f.theme_json or '{}'),'thank_you':json.loads(f.thank_you_json or '{}'),'questions':[public_question(q) for q in f.questions]}
@router.post('/public/forms/{slug}/responses')
def submit(slug:str,data:ResponseCreate,db:Session=Depends(get_db)):
 f=db.query(Form).filter(Form.slug==slug,Form.status=='published').first()
 if not f:raise HTTPException(404,'Published form not found')
 qmap={q.id:q for q in f.questions};provided={a.question_id:a.value for a in data.answers}
 for q in f.questions:validate(q,provided.get(q.id))
 for item in data.answers:
  if item.question_id not in qmap:raise HTTPException(422,'Unknown question')
 r=Response(form_id=f.id,submitted_at=datetime.utcnow());db.add(r);db.flush()
 for item in data.answers:
  v=item.value;a=Answer(response_id=r.id,question_id=item.question_id)
  if isinstance(v,bool):a.value_boolean=v
  elif isinstance(v,(int,float)):a.value_number=str(v)
  elif isinstance(v,(dict,list)):a.value_json=json.dumps(v)
  elif v is not None:a.value_text=str(v)
  db.add(a)
 db.commit();return {'ok':True,'response_id':r.id}
@router.get('/forms/{form_id}/responses')
def responses(form_id:int,db:Session=Depends(get_db)):
 f=db.get(Form,form_id)
 if not f:raise HTTPException(404,'Form not found')
 return [{'id':r.id,'submitted_at':r.submitted_at.isoformat(),'answers':[{'question_id':a.question_id,'value':value_for_answer(a)} for a in r.answers]} for r in f.responses]
@router.get('/forms/{form_id}/stats')
def stats(form_id:int,db:Session=Depends(get_db)):
 f=db.get(Form,form_id)
 if not f:raise HTTPException(404,'Form not found')
 output=[]
 for q in f.questions:
  counts={}
  if q.type in ('multiple_choice','dropdown','yes_no','rating'):
   for r in f.responses:
    a=next((x for x in r.answers if x.question_id==q.id),None)
    if a:
     v=value_for_answer(a);key=str(v);counts[key]=counts.get(key,0)+1
  output.append({'question_id':q.id,'title':q.title,'type':q.type,'counts':counts})
 return {'response_count':len(f.responses),'questions':output}
@router.get('/forms/{form_id}/responses/{response_id}')
def response_detail(form_id:int,response_id:int,db:Session=Depends(get_db)):
 r=db.query(Response).filter(Response.id==response_id,Response.form_id==form_id).first()
 if not r:raise HTTPException(404,'Response not found')
 return {'id':r.id,'submitted_at':r.submitted_at.isoformat(),'answers':[{'question_id':a.question_id,'value':value_for_answer(a)} for a in r.answers]}
