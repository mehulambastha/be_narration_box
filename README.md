# DueIT
We don't do hard deadlines here, let's cut down on anxiety and work for a healthier mind too. For this reason, we don't believe in edits, don't edit you task, do it! or delete it and start afresh. Redoing and changing, giving yourself more and more time are old habits, welcome to DueIt! Change begins with you.

## Catch it live
[live app](https://nb.mehul.pro/) | 
[backend documentation](https://api-nb.mehul.pro/docs)

## Tech Stack used
FastAPI, PostgresQL, Docker, Asyncpg, SQLAlchemy, Alembic, Pydantic 

## Architecture
The code structure of backend is - 
```
├── alembic
│   ├── env.py
├── alembic.ini
├── app
│   ├── api
│   │   ├── llm
│   │   │   ├── gen_todo.py
│   │   └── routers
│   │       ├── __init__.py
│   │       └── todos.py
│   ├── database.py
│   ├── dependencies.py
│   ├── __init__.py
│   ├── logging.py
│   ├── main.py
│   ├── models
│   │   └── todo.py
│   ├── schemas
│   │   └── todo.py
│   ├── services
│   │   ├── base.py
│   │   └── todo.py
│   └── sse
│       ├── event_queue.py
│       ├── events.py
│       └── verify.py
├── app.log
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── tests
```

The backend is fairly simple, and demonstrated scalable coding practices by following the SOC philosophy. The Backend consists of routes for creation / deletion / updation / and reading existing tasks.

## AI Integration
GroqAI is used for understanding user's goal and interpreting it, providing task breakdown according to the level chosen. User provides their desired goal and through fairly simple prompt engineering I get from LLM, the exact JSON structure that is required to create the tasks internally. From there on , it is a fairly simple part.

## Choices
- Chose postgres because of its speed and easy deployment, robustness and ability to tackle large scale to small scale, all kinds of data.
- Pydantic is used to maintain class based structure and enforce type safety, and also fundamentally important when interacting with databases through an ORM such as SQLAlchemy, which relies on its own class structure, and its own Columns, Rows and data types
- Alembic is another one tool which works great in combination with SQLAlchemy, providing easy SQL migrations.
Rest all are fairly standard tools.
- For deployment purposes and maintain safe and non penetrable architecture, the database itself run in the docker container, and not on the server as a whole. Peristent volume ensures the data stays in the database even during down time.
- Creation of separate user in the docker container ensures that even if the app is compromised, access does not go to root level , i.e., server level.

## What I wanted to implement and almost did
- Wanted to add an achievements section, which would simply listen to Server Side Events (SSE) and show user the notification.
- Set up the emit and stream routes but due to my own over-complication of things, couldn't ship this feature on time.

## How to run
- clone, create .env file through .env.example.
- Add relevant data in .env file
- Update the same in docker-compose and alembic/env.py file
- docker compose up --build -d
- All set!

## App images
![dueit1](https://github.com/user-attachments/assets/6afed00f-b305-47be-b1cd-fb24cc96bd5a)
![dueit2](https://github.com/user-attachments/assets/48d72aee-b899-485a-a801-164eefd44bcb)
![dueit3](https://github.com/user-attachments/assets/3c85a202-aca2-4c71-9851-9ce5b589ff96)
![dueit4](https://github.com/user-attachments/assets/3acd219d-bb6c-4882-b2ab-8e10f9503977)
![dueit5](https://github.com/user-attachments/assets/4746e709-ddb8-4ec6-a3de-89e081663dd9)
![dueit6](https://github.com/user-attachments/assets/b4554e98-7978-4eb3-80cf-b8911914e1c0)
![dueit7](https://github.com/user-attachments/assets/f0c0a9a3-44b5-4039-bdd7-17c0808f2a0f)
![dueit8](https://github.com/user-attachments/assets/8324239c-7a57-4ff1-866c-58aaf2e3b34e)
![dueit9](https://github.com/user-attachments/assets/051f8ffd-989f-4877-b0b9-de3fa20ab2ea)

  
