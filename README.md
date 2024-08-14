# Redash chat add-on

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Key Features](#key-features) 
- [Screenshots](#screenshots)
- [License](#license)

## Project Overview

Develop a Redash chat add-on facilitating conversation and autonomous knowledge discovery, empowering team members to extract insights from multiple Redash dashboards and connected databases using natural language. This add-on will empower users to ask questions about dashboard visuals, retrieve insights from existing data and visualizations automatically. The tool allows non-technical team members to easily extract and visualize data without extensive SQL knowledge, streamlining analytical processes and enhancing data exploration accessibility and efficiency

## Tech Stack

- **Programming Languages:** Python,
- **BAckend Framework:** Quart,
- **Frontend Framework:** Redash,

## Setup Instructions

### Prerequisites

- Python 3.x
- NodeJS 18
- yarn 1.22.22
- docker 

### Installation

1. **Clone the Repository**
   ```sh
   git clone git@github.com:jadmassu/chatbot_with_redash.git
   cd chatbot_with_redash
   ```

2. **Install Backend Requirements**

   ```sh
   pip install -r requirements.txt
   ```

3. **SetUP environments**
   ```sh
   OPENAI_API_KEY = Your_open_api_key
   BACKEND_API_URI = BACKEND_API_URI
   ```

## API Development

**Run Flask Application**

```sh
cd api 
poetry run start
```

## Redash


```sh
cd redash
make build
make compose_build
make up
```

**Open with your browser to see the result.**

[http://localhost:3000](http://localhost:5001)

## Project Structure

    ├── api
    │   ├── src   
    |   └── ...
    ├── scripts
    ├── redash                   # Redash source code with chat plugin
    ├── requirements.txt          # Python dependencies
    ├── README.md                 # Project documentation
    └── ...

## Key Features

* Redash Chat Add-On Integration: Integrated chat functionality into Redash.
* SQL Query Generation: Automatically generates SQL queries from chat inputs.
* Visualization Automation: Automatically creates visualizations based on generated SQL queries.

## Screenshots
![Screenshot from 2024-05-17 13-19-44](https://github.com/user-attachments/assets/23e3ccae-6db7-44b5-82b0-e4ddb6a68848) 

![Screenshot from 2024-05-17 13-17-38](https://github.com/user-attachments/assets/212e03a1-9f76-4e47-9a49-14384b49dd5a)


### License

This project is licensed under the MIT License. See the LICENSE file for details.
