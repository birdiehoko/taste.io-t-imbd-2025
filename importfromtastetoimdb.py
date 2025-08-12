import pandas as pd
from imdb import Cinemagoer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException  # ADD
import time

# Map Taste ratings to IMDb 1-10 scale (adjust as needed)
RATING_MAP = {
    1: 2,
    2: 5,
    3: 7,
    4: 10
}

# Load Taste ratings CSV
df = pd.read_csv('output.csv')  # Ensure this file exists

# Initialize Cinemagoer for IMDb ID lookup
ia = Cinemagoer()

# Set up Selenium with Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Log in to IMDb
driver.get('https://www.imdb.com/registration/signin')
time.sleep(2)

# Click "Sign in with IMDb" (adjust if you use Google/Facebook login)
try:
    driver.find_element(By.XPATH, '//span[text()="Sign in with IMDb"]').click()
    time.sleep(2)
    email_input = driver.find_element(By.ID, 'ap_email')
    email_input.send_keys('user@gmail.com')  # REPLACE
    password_input = driver.find_element(By.ID, 'ap_password')
    password_input.send_keys('password')  # REPLACE
    driver.find_element(By.ID, 'signInSubmit').click()
except:
    print("Adjust login steps for your method (e.g., Google/Facebook)")
    driver.quit()
    exit()
time.sleep(25)  # Wait for login

# Process each movie
for index, row in df.iterrows():
    title = row['name']
    year = row.get('year', '')  # Handle missing year
    taste_rating = row['rating']
    
    # Map to IMDb rating
    imdb_rating = RATING_MAP.get(taste_rating, 0)  # Default to 5 if unknown
    
    print(f"Processing: {title} ({year}) - Rating: {imdb_rating}")
    
    # Search for movie ID
    search_query = title
    if year:
        search_query += f" {year}"
    try:
        movies = ia.search_movie(search_query)
        if not movies:
            print(f"Movie not found: {title}")
            continue
        movie_id = movies[0].movieID  # First match (improve if needed)
    except Exception as e:
        print(f"Error searching {title}: {e}")
        continue
    
    # Go to movie page
    driver.get(f'https://www.imdb.com/title/tt{movie_id}/')
    time.sleep(3)
    
    try:
        wait = WebDriverWait(driver, 15)

        # Open the rating dialog (use data-testid, more stable)
        rate_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-testid="hero-rating-bar__user-rating"] button')
        ))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", rate_button)
        rate_button.click()
        time.sleep(1)

        # Wait for starbar to be present
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ipc-starbar')))

        # Click the star via JS to bypass overlay interception
        star_button = wait.until(EC.presence_of_element_located((
            By.XPATH,
            f'//button[@aria-label="Rate {imdb_rating}"]'
        )))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", star_button)
        driver.execute_script("arguments[0].click();", star_button)
        time.sleep(1)

        # Submit rating: try 'done-button' first, then fallback
        try:
            submit_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[data-testid="done-button"]')
            ))
        except TimeoutException:
            submit_btn = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                '//button[contains(@class,"ipc-rating-prompt__rate-button")]'
            )))

        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(1)

        print(f"Rated {title} successfully with {imdb_rating}")
    except Exception as e:
        print(f"Error rating {title}: {e}")
        continue

# Clean up
driver.quit()