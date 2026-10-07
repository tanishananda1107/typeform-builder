export type QuestionType='short_text'|'long_text'|'multiple_choice'|'dropdown'|'email'|'number'|'yes_no'|'rating';
export type Theme={background?:string;text?:string;accent?:string;button?:string;font?:string};
export type Question={id:number;position:number;type:QuestionType;title:string;description:string;required:boolean;settings:Record<string,any>};
export type Form={id:number;title:string;slug:string;description:string;status:'draft'|'published';response_count:number;questions:Question[];theme?:Theme;thank_you?:{title:string;description:string};};
export type ResponseRow={id:number;submitted_at:string;answers:{question_id:number;value:any}[]};
