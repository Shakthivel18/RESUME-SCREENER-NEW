# AI Interviewer System Guide

The NeuralHire AI Interviewer is a powerful feature that generates personalized technical interviews based on a candidate's resume and the specific job description.

## 🚀 How It Works

1.  **Analysis**: The system analyzes the candidate's resume and the target job description.
2.  **Generation**: Using Google's Gemini AI, it generates 10 tailored questions covering:
    *   Technical Skills
    *   Problem Solving
    *   Experience
    *   Behavioral traits
3.  **Conducting**: The recruiter (or candidate in self-mode) answers the questions.
4.  **Evaluation**: The AI evaluates each answer in real-time, providing:
    *   Score (1-10)
    *   Feedback
    *   Strengths
    *   Areas for Improvement

## 🎮 How to Use

1.  **Login** as a Recruiter (`admin` / `admin123`).
2.  **Run Analysis** on a job description.
3.  On any candidate card, click the **"🎤 Interview"** button (gold button).
4.  The Interview Modal will open.
5.  **Read the Question** (note the difficulty and focus area).
6.  **Type the Answer** (or have the candidate type/dictate).
7.  Click **"Submit Answer"**.
8.  Review the **AI Evaluation**.
9.  Proceed through all 10 questions.
10. Click **"Complete Interview"** to save the session.

## ⚙️ Configuration

The system uses the **Google Gemini API** for intelligence.

*   **API Key**: Configured in `res/ai_interviewer.py`.
*   **Fallback**: If the API is unreachable or the key is invalid, the system gracefully falls back to a predefined question bank ensuring no disruption.

## 📂 Data Storage

Interview sessions are saved as JSON files in the `interviews/` directory:
`interviews/{candidate_id}_{timestamp}.json`

Each file contains:
*   Candidate & Job Details
*   All Questions generated
*   Candidate Answers
*   AI Evaluations & Scores
*   Overall Session Score
