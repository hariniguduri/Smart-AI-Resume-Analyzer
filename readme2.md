# Smart AI Resume Analyzer - Complete Project Guide

## 1. Project Overview

Smart AI Resume Analyzer is a Streamlit-based web application for resume analysis, AI-assisted resume feedback, job-role alignment, and job-search support.

The project combines:

- Standard ATS-style resume analysis using rule-based logic
- AI-powered resume analysis using Google Gemini
- Resume parsing for PDF and DOCX files
- Role-based skill matching and recommendations
- Personalized course and interview resource suggestions
- Job search redirection across multiple job portals
- User authentication and per-user analysis history
- Local database storage using SQLite
- PDF report generation for AI analysis results

In short, this project is designed as an end-to-end career support tool where a user can log in, upload a resume, get analysis and feedback, explore improvement resources, search jobs, and keep a history of their results.

## 2. Main User Flows

### Authentication

Users first sign up or log in. Passwords are hashed before storage, and authenticated state is stored in Streamlit session state.

### Standard Resume Analyzer

The user:

1. Selects a job category and specific role
2. Uploads a PDF or DOCX resume
3. Gets:
   - ATS score
   - Keyword match score
   - Format score
   - Section score
   - Missing skills
   - Improvement suggestions
4. Receives related courses and video recommendations
5. Has analysis data saved locally in SQLite

### AI Resume Analyzer

The user:

1. Selects a role
2. Uploads a resume
3. Optionally pastes a real job description
4. Sends the extracted resume text to Google Gemini
5. Receives:
   - Detailed markdown analysis
   - Resume score
   - ATS score
   - Role alignment feedback
   - Optional job-description match guidance
6. Can download a PDF report
7. Has AI analysis statistics stored in SQLite

### Job Search

The user enters a job title and location, and the app generates job links for multiple platforms such as LinkedIn, Naukri, Foundit, FreshersWorld, TimesJobs, Instahyre, and Indeed.

### History

Logged-in users can review and delete their saved analysis history.

## 3. Core Technology Stack

- Frontend/UI: Streamlit, custom CSS, Plotly
- Backend logic: Python
- AI integration: Google Gemini via `google-generativeai`
- Resume parsing: `pypdf`, `PyPDF2`, `pdfplumber`, `python-docx`, `docx2txt`
- OCR fallback for scanned PDFs: `pdf2image`, `pytesseract`
- Database: SQLite, SQLAlchemy, sqlite3
- Data handling: pandas, openpyxl, numpy
- Report generation: reportlab
- Styling and media: Pillow, Lottie, Font Awesome, Google Fonts

## 4. Architecture Summary

The architecture is centered around `app.py`, which creates the Streamlit application and coordinates all modules.

### Flow

1. `app.py` initializes session state, authentication, database setup, CSS, and analyzers
2. Uploaded resumes are validated in `streamlit_utils.py`
3. Resume text is extracted by:
   - `utils/resume_analyzer.py`
   - `utils/resume_parser.py`
   - `utils/ai_resume_analyzer.py` as a fallback for difficult PDFs
4. Standard analysis is performed using keyword, section, and formatting heuristics
5. AI analysis is performed using Gemini with a structured prompt
6. Results are saved into SQLite through:
   - `config/database.py`
   - `models.py`
   - `streamlit_utils.py`
7. Job recommendations, courses, and videos come from `config/` and `jobs/`

## 5. Key Functional Modules

### Standard Resume Analysis

Handled mainly by `utils/resume_analyzer.py`.

It includes:

- Document type detection
- Keyword matching against required role skills
- Contact/summary/skills/experience/education checks
- Formatting checks
- ATS score calculation
- Structured suggestions generation

This is a deterministic rule-based analyzer, not an LLM-based one.

### AI Resume Analysis

Handled by `utils/ai_resume_analyzer.py`.

It includes:

- PDF and DOCX text extraction
- OCR fallback for scanned PDFs
- Gemini prompt construction
- Parsing of AI response for resume score and ATS score
- PDF report generation
- Structured section processing for the downloadable report

### Authentication

Handled by `auth.py` and `models.py`.

It includes:

- Signup
- Login
- Password hashing with PBKDF2-HMAC SHA-256
- Session tracking
- Current-user retrieval
- Per-user history linkage

### Database Layers

This project uses multiple database access patterns:

- `models.py`: SQLAlchemy models for users and user-linked analysis history
- `config/database.py`: sqlite3 helpers for resume records, admin data, and AI stats
- `utils/database.py`: a second SQLAlchemy-based manager for resumes and analyses

This works, but it also means the project has overlapping database responsibilities across files.

### Job Search

Handled by `jobs/job_search.py`, `jobs/job_portals.py`, and `jobs/suggestions.py`.

It includes:

- Search term suggestions
- Location suggestions with Indian states/cities and work modes
- Experience filters
- Job portal URL generation

### Learning Recommendations

Handled by `config/courses.py`.

It provides:

- Role-based course suggestions
- Resume improvement videos
- Interview preparation videos

### UI Helpers

Handled by `ui_components.py` and `style/style.css`.

These files provide reusable cards, headers, metrics, feature layouts, and the dark-themed look and feel of the application.

## 6. Databases and Stored Data

The repository already contains local database files:

- `resume_data.db`
- `resume_analysis.db`

The application stores:

- User accounts
- Saved analysis history
- Resume metadata
- Standard analysis results
- AI analysis usage stats
- Admin logs and admin credentials

There is also:

- `resume_data_export.xlsx`: exported resume data sample/output

## 7. Environment and API Keys

The AI analyzer expects secrets from environment variables, typically through a `.env` file.

Important variables:

- `GOOGLE_API_KEY`
- `OPENROUTER_API_KEY` (present in code, but Gemini is the active analyzer in the UI)

Note:

- The repository contains `utils/.env`, which suggests local secret storage has been used during development.
- Secrets should not be committed to public repositories.

## 8. How to Run the Project

### Recommended local steps

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

### Alternative launcher

```bash
python run_app.py
```

`run_app.py` attempts to run a `setup_chromedriver.py` script if it exists and then launches Streamlit.

## 9. Important Project Observations

- The app is login-protected before users can access analyzer features.
- The standard analyzer and AI analyzer are both active and serve different purposes.
- The AI analyzer currently exposes only Google Gemini in the UI.
- The codebase contains multiple database helper layers that overlap in responsibility.
- Some files and docs reference older or broader functionality than what is currently wired into the Streamlit UI.
- `run_app.py` references `setup_chromedriver.py`, but that file is not present in the current repository snapshot.
- The repository includes generated/runtime artifacts such as databases, Excel output, and `__pycache__` folders.

## 10. File-by-File Project Explanation

Below is a practical explanation of the visible repository files and folders.

### Top-level files

#### `app.py`

Main Streamlit application.

Responsibilities:

- Sets Streamlit page configuration
- Initializes the app class
- Loads CSS and fonts
- Handles login gating
- Renders:
  - Home page
  - Standard analyzer
  - AI analyzer
  - Job search page
  - User history
- Stores analysis results in databases
- Generates UI for scores, statistics, videos, and downloads

This is the central file of the project.

#### `auth.py`

Authentication helper module.

Responsibilities:

- Initializes auth session state
- Hashes passwords securely
- Verifies passwords
- Handles signup/login/logout
- Retrieves the current logged-in user

#### `models.py`

SQLAlchemy models for authentication and history storage.

Tables represented:

- `users`
- `resume_analyses`

Responsibilities:

- Creates database engine
- Defines ORM models
- Initializes tables
- Exposes DB session factory

#### `streamlit_utils.py`

Streamlit-side utility helpers.

Responsibilities:

- Validates uploaded resume files
- Cleans and formats skill values for storage
- Saves user-linked analysis history
- Returns history as a pandas DataFrame
- Deletes history entries

#### `ui_components.py`

Reusable UI rendering helpers.

Responsibilities:

- Page headers
- Hero sections
- Feature cards
- Metric cards
- Template cards
- Feedback cards
- Progress bars
- Alerts
- Simple layout helpers

Note:

- This file contains overlapping `about_section` definitions, so one function overrides the earlier one.

#### `run_app.py`

Helper launcher script.

Responsibilities:

- Tries to execute chromedriver setup if available
- Starts the app with `python -m streamlit run app.py`

#### `README.md`

Original project README with feature marketing, setup notes, screenshots, and public-project presentation.

#### `readme2.md`

This file. A repo-focused explanation of the current project structure and implementation.

#### `requirements.txt`

Python dependency list for the app.

Includes packages for:

- Streamlit UI
- NLP
- PDF/DOCX parsing
- AI integrations
- plotting
- OCR
- reporting
- database work

#### `packages.txt`

System packages for environments like Streamlit Cloud or Linux deployments.

Used for browser/headless or PDF support dependencies such as:

- `chromium`
- `chromium-driver`
- `xvfb`
- `wget`
- `unzip`

#### `how_to_run.txt`

Local run notes, especially focused on using a specific environment and installing `google-generativeai`.

#### `AI_MODELS.md`

Explains the AI model usage conceptually, mainly focused on Gemini.

#### `DEPLOYMENT.md`

Deployment notes for local, server, Streamlit Cloud, and Docker setups.

#### `SECURITY.md`

Security-themed repo note.

#### `LICENSE`

Project license file.

#### `.gitignore`

Git ignore rules for files and folders that should not be committed.

#### `architecture.png`

Architecture diagram image for the project.

#### `resume_analysis.db`

Local SQLite database file.

Likely stores analysis-related runtime data.

#### `resume_data.db`

Main local SQLite database file actively referenced by multiple modules.

#### `resume_data_export.xlsx`

Excel export/output file containing saved resume-related data.

### Folder: `.github/`

#### `.github/CODE_OF_CONDUCT.md`

Community behavior and participation guidelines.

#### `.github/CONTRIBUTING.md`

Contribution guidance for collaborators.

#### `.github/FUNDING.yml`

Funding/support configuration for GitHub.

### Folder: `assets/`

#### `assets/logo.jpg`

Branding/logo image used by the project or documentation.

#### `assets/124852522.jpeg`

Additional image asset used by the UI or docs.

### Folder: `style/`

#### `style/style.css`

Primary CSS stylesheet for the Streamlit app.

Responsibilities:

- Theme colors
- Typography
- input and button styling
- card styling
- dark-mode presentation
- component-level visual customization

### Folder: `config/`

#### `config/job_roles.py`

Core role-definition map for the analyzer.

Stores:

- job categories
- specific roles
- required skills
- recommended sections
- recommended technical/soft skills
- descriptions

This file is what drives the role selection menus and keyword matching expectations.

#### `config/courses.py`

Learning-resource configuration.

Stores:

- role-based course lists
- resume-related videos
- interview-related videos

Also provides helper functions to map a role to its category and course list.

#### `config/database.py`

sqlite3-based database helper layer.

Responsibilities:

- initializes tables
- saves resume data
- saves standard analysis data
- logs admin activity
- verifies/adds admins
- saves AI analysis data
- calculates AI analysis statistics
- returns aggregated dashboard data

Tables managed here include:

- `resume_data`
- `resume_skills`
- `resume_analysis`
- `admin_logs`
- `admin`
- `ai_analysis`

### Folder: `jobs/`

#### `jobs/job_search.py`

Renders the job search UI page.

Responsibilities:

- text inputs for job title and location
- suggestion filtering
- advanced filters
- portal results cards
- tabbed job-search interface

#### `jobs/job_portals.py`

Portal URL generator and formatter.

Responsibilities:

- defines supported job portals
- formats job titles and locations
- maps experience filters into portal-specific query parameters
- returns a list of clickable search result links

#### `jobs/suggestions.py`

Static job and location suggestion data.

Contains:

- job title suggestions
- work mode suggestions
- Indian state and city suggestions
- job type options
- experience ranges
- salary ranges

### Folder: `resume_analytics/`

#### `resume_analytics/analyzer.py`

An additional NLP-oriented analyzer using spaCy.

Responsibilities:

- word count
- sentence count
- skill extraction
- years-of-experience estimation
- profile scoring
- suggestion generation

This appears to be a separate analytics module and is not the main analyzer currently used by `app.py`.

### Folder: `utils/`

#### `utils/__init__.py`

Package initializer for utility modules.

Exports:

- `ResumeAnalyzer`
- `ResumeParser`
- `ExcelManager`
- database helpers
- `AIResumeAnalyzer`

#### `utils/resume_parser.py`

Basic resume text parser.

Responsibilities:

- extract text from PDF and DOCX
- detect a small fixed set of skills
- return a simple parsed dictionary

This is a lightweight parser compared with the larger rule-based analyzer.

#### `utils/resume_analyzer.py`

Main rule-based standard analyzer used by the Streamlit app.

Responsibilities:

- document type detection
- keyword match scoring
- contact/education/experience/project/skills/summary extraction
- formatting checks
- section checks
- ATS score calculation
- detailed suggestions

This is one of the most important logic files in the project.

#### `utils/ai_resume_analyzer.py`

Main AI analysis engine.

Responsibilities:

- extract resume text from PDF/DOCX
- use OCR when needed
- call Gemini
- format structured AI prompts
- read scores from AI text
- generate rich PDF reports
- process report sections for display/export

This is the second most important logic file after `app.py`.

#### `utils/database.py`

Another database helper layer using SQLAlchemy.

Responsibilities:

- define `Resume`, `Analysis`, and `AIAnalysis`
- save and query resumes
- save analysis records
- return AI analysis statistics

This overlaps with `config/database.py`, so it is useful to know both exist.

#### `utils/excel_manager.py`

Excel export helper.

Responsibilities:

- store resume entries in an Excel workbook
- fetch all resumes
- fetch user-specific resumes from the workbook

#### `utils/Admin.png`

Image asset, likely intended for admin-related UI or branding.

#### `utils/.env`

Local environment file for secrets/config.

It should contain API keys or environment-specific values and should be treated as sensitive.

### Folders: `__pycache__/`, `config/__pycache__/`, `jobs/__pycache__/`, `resume_analytics/__pycache__/`, `utils/__pycache__/`

These are Python bytecode cache directories created automatically during execution.

They are not source code and can usually be ignored for documentation and version control.

## 11. Practical Strengths of This Project

- Covers both traditional ATS-style logic and modern AI analysis
- Has a usable multi-page Streamlit UI
- Includes login and per-user history
- Gives job-role-specific recommendations
- Adds learning resources instead of only giving a score
- Supports job-search redirection from inside the app
- Produces downloadable PDF reports for AI analysis

## 12. Practical Limitations and Maintenance Notes

- There are multiple database helper systems, which increases maintenance complexity
- Some files appear partially redundant or legacy
- Some deployment notes mention scripts not present in the current repo snapshot
- OCR and AI features depend on additional local/system setup
- Secrets handling should be tightened if the project is published
- Some UI helper functions overlap or are duplicated

## 13. Best Short Description of the Project

Smart AI Resume Analyzer is a Streamlit web app that helps users upload a resume, compare it against job-role expectations, receive ATS and AI-based feedback, explore learning resources, search jobs, and store their analysis history locally.
