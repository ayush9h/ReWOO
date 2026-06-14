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





# Human In The Loop - Acceptance
<img width="1051" height="915" alt="image" src="https://github.com/user-attachments/assets/435599c9-df52-4243-a732-c067606ccb1a" />
<img width="1081" height="912" alt="image" src="https://github.com/user-attachments/assets/b0f1486e-8ea2-4ddd-a514-d193dbc29fad" />


# Human In the Loop - Reject
<img width="1048" height="911" alt="image" src="https://github.com/user-attachments/assets/8b38f86e-4a4f-4e54-8a30-afa8622abfb6" />


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
