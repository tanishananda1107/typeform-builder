# Formly — Typeform Builder

A full-stack Typeform-inspired form builder built for the SDE Fullstack Assignment. It implements the required creator workflow, drag-and-drop builder, publishing, public conversational respondent experience, validation, response persistence, results, analytics, seeded demo data, and CSV export.

## Stack

- Frontend: Next.js + TypeScript + React + Framer Motion + dnd-kit
- Backend: FastAPI + SQLAlchemy + Pydantic
- Database: SQLite
- Styling: custom CSS designed around Typeform-like whitespace, typography, focus, and conversational interactions

## Features

### Form Builder
- Create forms
- Edit form title/description
- Add 8 required question types
- Edit question text and help text
- Required toggle
- Choice/dropdown options
- Rating min/max
- Drag-and-drop reorder
- Delete questions
- Live preview
- Preview mode without persisting responses

### Form Management
- Dashboard
- Draft/published status
- Response counts
- Rename
- Duplicate
- Delete
- Publish/unpublish
- Shareable public slug

### Respondent Experience
- No authentication required
- One question at a time
- Full-screen layout
- Animated transitions
- Progress indicator
- Back navigation
- Enter/arrow keyboard navigation
- Client-side validation
- Server-side validation
- Thank-you screen

### Results
- Response table
- Individual response modal
- Per-question counts for choice/rating/yes-no questions
- CSV export
- Persistent responses

### UX polish
- Toast notifications
- Inline editing
- Responsive layout
- Typeform-inspired builder canvas
- Theme and thank-you configuration persisted in the database/API
- Placeholder-ready architecture for logic, integrations, teams and advanced question types

## Database

```text
Creator 1 ──── * Form
Form 1 ──── * Question
Form 1 ──── * Response
Response 1 ──── * Answer
Question 1 ──── * Answer
```

Tables:

- `creators`
- `forms`
- `questions`
- `responses`
- `answers`

Questions and answers are normalized rather than stored as one large JSON object. This allows response queries and statistics without parsing an entire form document.

## API

### Forms

- `GET /api/forms`
- `POST /api/forms`
- `GET /api/forms/{id}`
- `PATCH /api/forms/{id}`
- `DELETE /api/forms/{id}`
- `POST /api/forms/{id}/duplicate`
- `POST /api/forms/{id}/publish`
- `POST /api/forms/{id}/unpublish`

### Questions

- `POST /api/forms/{id}/questions`
- `PATCH /api/questions/{id}`
- `DELETE /api/questions/{id}`
- `PATCH /api/forms/{id}/questions/reorder`

### Public

- `GET /api/public/forms/{slug}`
- `POST /api/public/forms/{slug}/responses`

### Results

- `GET /api/forms/{id}/responses`
- `GET /api/forms/{id}/responses/{responseId}`
- `GET /api/forms/{id}/stats`

Interactive API documentation is available at `/docs` when FastAPI is running.

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Backend: `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:3000`

Set `NEXT_PUBLIC_API_URL` if the backend is deployed somewhere else.

## Docker

From the repository root:

```bash
docker compose up --build
```

## Seed data

The backend automatically seeds two published forms on a fresh database:

1. Customer Feedback — mixed text, email, choice, rating, yes/no and long text questions with 8 responses.
2. Developer Survey — text, number, dropdown, choice, rating and yes/no questions with 6 responses.

## Assumptions

- Creator authentication is intentionally simplified to a default creator as permitted by the assignment.
- SQLite is appropriate for the evaluation/demo deployment.
- Advanced branching, integrations, teams, payments and file uploads are outside the required scope.
- The UI is an original implementation inspired by Typeform interaction patterns rather than copied source code/assets.

## Evaluation walkthrough

1. Open dashboard and inspect seeded forms.
2. Open a form in Builder.
3. Add each question type.
4. Drag questions to reorder them.
5. Edit title, description, required state and choice options.
6. Preview the form.
7. Publish it.
8. Open the generated public share URL.
9. Complete the one-question-at-a-time form using keyboard navigation.
10. Open Results and inspect the response.
11. Inspect question summary statistics.
12. Export CSV.
13. Duplicate and rename a form.

## Interview discussion points

- Why normalized relational tables were used.
- Why public respondent endpoints are separated from creator endpoints.
- Why server validation duplicates client validation.
- How drag-and-drop order is persisted.
- How the same question renderer is reused by preview and respondent mode.
- How the respondent state machine moves from question to question.
- How response statistics are derived.
