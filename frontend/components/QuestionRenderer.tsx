'use client';
import {Question} from '../lib/types';
export default function QuestionRenderer({question,value,onChange,disabled=false}:{question:Question;value:any;onChange:(v:any)=>void;disabled?:boolean}){
 const common=(placeholder='Type your answer...')=><input disabled={disabled} className="field" placeholder={placeholder} value={value??''} onChange={e=>onChange(e.target.value)}/>;
 if(question.type==='long_text') return <textarea disabled={disabled} className="textarea" placeholder="Type your answer..." value={value??''} onChange={e=>onChange(e.target.value)}/>;
 if(question.type==='email') return common('name@example.com');
 if(question.type==='number') return <input disabled={disabled} className="field" type="number" placeholder="0" value={value??''} onChange={e=>onChange(e.target.value===''?'':Number(e.target.value))}/>;
 if(question.type==='dropdown') return <select disabled={disabled} className="input" value={value??''} onChange={e=>onChange(e.target.value)}><option value="">Select an option</option>{(question.settings.options||[]).map((x:string)=><option key={x}>{x}</option>)}</select>;
 if(question.type==='multiple_choice'||question.type==='yes_no'){const opts=question.type==='yes_no'?['Yes','No']:(question.settings.options||[]);return <div>{opts.map((x:string)=><button disabled={disabled} type="button" key={x} className={`option ${value===x?'selected':''}`} onClick={()=>onChange(x)}>{x}</button>)}</div>}
 if(question.type==='rating'){const min=Number(question.settings.min??1),max=Number(question.settings.max??5);return <div className="rating">{Array.from({length:max-min+1},(_,i)=>i+min).map(n=><button disabled={disabled} type="button" className={value===n?'selected':''} key={n} onClick={()=>onChange(n)}>{n}</button>)}</div>}
 return common();
}
