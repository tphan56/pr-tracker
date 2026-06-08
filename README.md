# Personal Record Tracker
Fun project to track personal records (PR) for gym exercises I have done. Purpose is to not only track my fitness and progress in the gym, but build upon my web development skills by making a personalized website, and dip my feet into API and backend work using Python.


<img width="3024" height="1696" alt="image" src="https://github.com/user-attachments/assets/485d4740-c80d-4f3a-b2c6-18b4ba65e346" />

<img width="1512" height="767" alt="Screenshot 2026-06-08 at 3 05 10 PM" src="https://github.com/user-attachments/assets/92155155-5919-42a1-ab87-920c5cd2af1d" />


## How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/tphan56/pr-tracker.git
cd pr-tracker
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows, use:

```bash
venv\Scripts\activate
```

3. Install the required Python packages:

```bash
pip install flask requests
```

4. Set up your API key.

This project uses the API Ninjas Exercise API to check whether an entered exercise is valid. Create a `.env` file or environment variable for your API key.

For macOS/Linux:

```bash
export API_NINJAS_KEY="your_api_key_here"
```

For Windows PowerShell:

```powershell
$env:API_NINJAS_KEY="your_api_key_here"
```

5. Run the app:

```bash
python App.py
```

6. Open the website in your browser:

```text
http://127.0.0.1:5050
```

The app will automatically create the local SQLite database file, `prs.db`, if it does not already exist.

