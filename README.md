# AI-Based Audio Analyzer App

This is an AI-based audio analyzer app.

Within the scope of this technical specification, you need to implement the logic for audio analysis—breaking the audio into prompts that can then be used to create images in MidJourney or another image generation service. You can use any APIs; I used ASSEMBLYAI for converting audio to text and Langchain for generating prompts.

## How to Run the Program

1. First, you need to fill the `.env` file with your data. The `API_KEY_ASSEMBLYAI` can be obtained for free by visiting their website: [AssemblyAI](https://www.assemblyai.com/?utm_source=google&utm_medium=cpc&utm_campaign=Brand&utm_term=assemblyai&gad_source=1&gclid=Cj0KCQjwpvK4BhDUARIsADHt9sQMQ4K4qMwvLGveqdzjOFkSfTB81-_CTJVeZaV-DUXvqQh6DihFLwQaAkCmEALw_wcB).
   
2. [Example of data](https://github.com/user-attachments/assets/fe42173b-4df5-4242-bd8e-4bcaa24e1748) if you want to run it with Docker Compose.

3. Then fill the `docker-compose.env` file (if you want it to run via Docker Compose).

4. [Another example](https://github.com/user-attachments/assets/b7064b81-9643-45f2-a3a7-1f7668f3a8c1).

5. Finally, run `docker-compose up --build` and wait for it to start.

## What I Have Implemented

1. Full reliable JWT authentication with login, logout, and registration with reliable validation.
2. Protected endpoints only for authorized users.
3. Ability to create prompt tasks both with audio files and text.
4. Optimized queryset to avoid the N+1 problem and a reliable database schema.
5. Pagination to avoid large querysets.
6. Docker and Docker Compose files.
7. CRUD operations for the analyzer task, including bulk update/destroy, optimized for large datasets.

## Documentation

1. Created Swagger documentation for endpoints via this link: [Swagger Documentation](http://127.0.0.1:8000/swagger/schema/).

## What I Did Not Manage to Do

1. I did not  manage to implement bulk update from prompts through nested serialization, so it is currently read-only.
2. I planned to put the logic of converting audio and creating LLM prompts into Celery tasks (you may even see its configuration), but I decided not to do it for now.
