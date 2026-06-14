## ReWOO(**Re**asoning **W**ith**O**ut **O**bservation)


LangGraph implementation of the ReWOO(Reasoning without Observation) framework along with Human In The Loop pattern.

[Research Article Link](https://arxiv.org/abs/2305.18323)

## Workflow

**ReWOO** introduces a *plan-and-execute* paradigm where the *workflow*

- Generates a structured execution plan
- Executes steps using tools with dependency awareness with human in the loop for tools required approval  
- Produces a final, user-facing response.


```
User Query
    ↓
Planner Node (LLM)
    ↓
Structured Plan (Steps + Dependencies)
    ↓
Executor Node (Async Execution) + Human In the Loop
    ↓
Tool Outputs (Evidence)
    ↓
Summarizer Node (LLM)
    ↓
Final Response
```
<img width="1397" height="417" alt="image" src="https://github.com/user-attachments/assets/985651f9-8bfd-4c21-9a13-827457bb58f2" />





## Human In The Loop - Acceptance
<img width="1307" height="915" alt="image" src="https://github.com/user-attachments/assets/3370c97d-9469-45fd-9862-1a3f3a6d61b4" />
<img width="1162" height="915" alt="image" src="https://github.com/user-attachments/assets/795ee8ef-1c81-40de-bf89-c5c97c58d082" />


## Human In the Loop - Reject
<img width="1207" height="912" alt="image" src="https://github.com/user-attachments/assets/7d20269c-9eca-4734-9b95-8de42675f1dc" />



## Usage

### Backend
- Setup environment
```
uv sync
```
- Script Execution
```
uvicorn main:app
```

### Frontend
- Install packages
```
npm install
```

- Run NextJs
```
npm run dev
```


## License
[MIT License](https://github.com/ayush9h/ReWOO?tab=MIT-1-ov-file)
