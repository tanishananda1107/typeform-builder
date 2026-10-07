import json,random
from datetime import datetime,timedelta
from .database import Base,engine,SessionLocal
from .models import Creator,Form,Question,Response,Answer

def seed():
 Base.metadata.create_all(bind=engine);db=SessionLocal()
 if db.query(Form).count():db.close();return
 c=Creator(name='Demo Creator',email='demo@example.com');db.add(c);db.flush()
 def add_form(title,slug,questions,description=''):
  f=Form(creator_id=c.id,title=title,slug=slug,status='published',description=description,theme_json=json.dumps({'background':'#ffffff','text':'#171717','accent':'#171717'}),thank_you_json=json.dumps({'title':'Thank you!','description':'Your response has been recorded.'}));db.add(f);db.flush()
  for i,q in enumerate(questions):db.add(Question(form_id=f.id,position=i,**q))
  return f
 f1=add_form('Customer Feedback','customer-feedback-demo',[
  dict(type='short_text',title="What's your name?",description="Let's start with your name.",required=True,settings_json='{}'),
  dict(type='email',title="What's your email?",description="We'll only use this for follow-up.",required=True,settings_json='{}'),
  dict(type='multiple_choice',title='What best describes your experience?',description='',required=True,settings_json=json.dumps({'options':['Excellent','Good','Okay','Poor']})),
  dict(type='rating',title='How would you rate our service?',description='1 is lowest, 5 is highest.',required=True,settings_json=json.dumps({'min':1,'max':5})),
  dict(type='yes_no',title='Would you recommend us?',description='',required=True,settings_json='{}'),
  dict(type='long_text',title="Anything else you'd like to share?",description='Optional feedback is welcome.',required=False,settings_json='{}')], 'A polished sample feedback form.')
 f2=add_form('Developer Survey','developer-survey-demo',[
  dict(type='short_text',title="What's your name?",description='',required=True,settings_json='{}'),
  dict(type='number',title='Years of experience?',description='',required=True,settings_json='{}'),
  dict(type='dropdown',title='Primary language?',description='',required=True,settings_json=json.dumps({'options':['TypeScript','Python','Java','Go','C++']})),
  dict(type='multiple_choice',title='Where do you work?',description='',required=True,settings_json=json.dumps({'options':['Remote','Office','Hybrid']})),
  dict(type='rating',title='Rate your developer setup',description='',required=True,settings_json=json.dumps({'min':1,'max':5})),
  dict(type='yes_no',title='Would you recommend your current stack?',description='',required=True,settings_json='{}')])
 names=['Tanisha','Rahul','Priya','Arjun','Meera','Karan','Aditi','Vikram']
 for idx,name in enumerate(names):
  r=Response(form_id=f1.id,submitted_at=datetime.utcnow()-timedelta(days=idx));db.add(r);db.flush();vals=[name,f'{name.lower()}@example.com',random.choice(['Excellent','Good','Okay']),random.randint(3,5),random.choice([True,False]),'Great experience!' if idx%2==0 else '']
  for q,v in zip(f1.questions,vals):
   a=Answer(response_id=r.id,question_id=q.id);setv(a,v);db.add(a)
 for idx,name in enumerate(names[:6]):
  r=Response(form_id=f2.id,submitted_at=datetime.utcnow()-timedelta(days=idx));db.add(r);db.flush();vals=[name,random.randint(1,8),random.choice(['TypeScript','Python','Java']),random.choice(['Remote','Office','Hybrid']),random.randint(3,5),random.choice([True,False])]
  for q,v in zip(f2.questions,vals):a=Answer(response_id=r.id,question_id=q.id);setv(a,v);db.add(a)
 db.commit();db.close()
def setv(a,v):
 if isinstance(v,bool):a.value_boolean=v
 elif isinstance(v,(int,float)):a.value_number=str(v)
 else:a.value_text=str(v)
