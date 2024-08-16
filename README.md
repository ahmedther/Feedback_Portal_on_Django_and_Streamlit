## Feedback Portal

### Overview

A comprehensive web application designed to collect and analyze feedback from discharged patients of a hospital. The project is divided into three main components:

### Key Features

- **Automated SMS System**: Implemented a Python script that runs hourly, sending SMS messages to recently discharged patients. Each message includes a personalized link to the feedback portal.
- **Feedback Web Application**: Created a dynamic, emoji-based UI where patients can provide feedback. The portal includes an admin panel, allowing administrators to create departments and modify questions as needed. Upon submission of feedback, an automated email is dispatched to the relevant departments for review.
- **Data Analysis Portal**: Constructed a separate data analysis portal using the Streamlit framework and Python. This portal, accessible only by authorized departments, allows for in-depth review of feedback data.

### Technologies Used

- **Front-End**: JavaScript, HTML, CSS, Streamlit
- **Back-End**: Python, Django, psycopg2
- **Database**: PostgreSQL, Oracle
- **Data Processing**: Pandas, NumPy
- **Deployment**: Docker, Kubernetes, Nginx
