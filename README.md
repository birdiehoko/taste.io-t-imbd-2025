# taste.io t imbd 2025

## instructions
1. **Get your Taste.io ratings:**
   - Go to your Taste.io profile in your web browser.
   - Open Developer Tools (usually F12 or right-click → "Inspect").
   - Find the element that contains your ratings (look for a `<div>` with your movie/show list).
   - Right-click on the correct element and choose "Copy" → "Copy element".
   - Paste the copied HTML into a new file named `element.html` in this folder.

2. **Install required Python packages:**
   ```
   pip install -r requirements.txt
   ```

3. **Extract your ratings to CSV:**
   - Run the following command:
     ```
     python taste.py
     ```
   - This will create a file called `output.csv` with your movie/show names and ratings.

4. **Prepare to import your ratings to IMDb:**
   - Open `importfromtastetoimdb.py` in a text editor.
   - Find the lines:
     ```
     email_input.send_keys('user@gmail.com')  # REPLACE
     password_input.send_keys('password')  # REPLACE
     ```
   - Replace `'user@gmail.com'` and `'password'` with your actual IMDb email and password.

5. **Handle IMDb login:**
   - When you run the script, a browser window will open and log in to IMDb.
   - If a captcha appears, you will have 25 seconds to solve it manually. After that, the script will continue and should not ask again.

6. **Automatically rate your titles on IMDb:**
   - Run:
     ```
     python importfromtastetoimdb.py
     ```
   - The script will process each title in your `output.csv` and rate it on IMDb automatically.
   - You can use your computer for other tasks while this runs.

**Note:** Make sure you are using the correct IMDb login method (the script is set up for standard IMDb login, not Google/Facebook). Adjust the login steps in the script if needed.
