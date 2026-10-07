from typing import Any,Optional
from pydantic import BaseModel,Field
class FormCreate(BaseModel): title:str=Field(min_length=1,max_length=255)
class FormUpdate(BaseModel): title:Optional[str]=None;description:Optional[str]=None;theme:Optional[dict[str,Any]]=None;thank_you:Optional[dict[str,str]]=None
class QuestionCreate(BaseModel): type:str;title:str='Untitled question';description:str='';required:bool=True;settings:dict[str,Any]={}
class QuestionUpdate(BaseModel): type:Optional[str]=None;title:Optional[str]=None;description:Optional[str]=None;required:Optional[bool]=None;settings:Optional[dict[str,Any]]=None
class Reorder(BaseModel): question_ids:list[int]
class AnswerIn(BaseModel): question_id:int;value:Any=None
class ResponseCreate(BaseModel): answers:list[AnswerIn]
