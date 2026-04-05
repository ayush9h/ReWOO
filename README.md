## ReWOO(**Re**asoning **W**ith**O**ut **O**bservation)

LangGraph implementation of the ReWOO(Reasoning without Observation) framework.

[Research Article Link](https://arxiv.org/abs/2305.18323)

## Workflow

**ReWOO** introduces a *plan-and-execute* paradigm where the *workflow*

- Generates a structured execution plan
- Executes steps using tools with dependency awareness  
- Produces a final, user-facing response.


```
User Query
    ↓
Planner Node (LLM)
    ↓
Structured Plan (Steps + Dependencies)
    ↓
Executor Node (Async Execution)
    ↓
Tool Outputs (Evidence)
    ↓
Summarizer Node (LLM)
    ↓
Final Response
```

### Response
![Response UI](https://github.com/user-attachments/assets/0efb4e10-5007-417c-9919-5bbea167e095)


### Execution Workflow
![Steps UI](https://github.com/user-attachments/assets/752f394e-8c2a-4ee1-9ff2-4da78639dc8c)


## Usage

- Setup environment
```
uv venv .venv
.venv/Scripts/activate
```
- Install Dependencies
```
uv pip install -r requirements.txt
```
- Script Execution
```
python app.py
```


## License
[MIT License](https://github.com/ayush9h/ReWOO?tab=MIT-1-ov-file)