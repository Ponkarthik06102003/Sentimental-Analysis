from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
# nltk.download('vader_lexicon')

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores['compound']

    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Set up the appropriate web driver based on user input
driver = None
user_choice = input("Are you an iOS or Android user? ")
if user_choice.lower() == "ios":
    app_name = input("Enter the name of the app or game (Please give the correct name for better results): ")
    # Use appropriate web driver for iOS (e.g., Safari)
elif user_choice.lower() == "android":
    app_name = input("Enter the name of the app or game (Please give the correct name for better results): ")
    # Use appropriate web driver for Android (e.g., Chrome)
else:
    print("Invalid choice. Please select either 'iOS' or 'Android'.")
    exit()

# Prompt the user to enter the name of the app or game
driver = webdriver.Chrome()

# Navigate to the respective app store and search for the app/game
if user_choice.lower() == "ios":
    driver.get("https://www.apple.com/app-store/")
    # Write code to search for the app/game using the provided name on the iOS app store
    # Use appropriate Selenium commands to interact with the web page elements
    search = driver.find_element(By.CSS_SELECTOR, '#globalnav-menubutton-link-search').click()
    sleep(2)
    search_box = driver.find_element(By.XPATH, '//*[@id="globalnav-submenu-search"]/div/div/form/div[1]/input[1]')
    search_box.send_keys("stack ball")
    sleep(2)
    search_box.send_keys(Keys.RETURN)
    sleep(2)
    driver.find_element(By.XPATH, '//*[@id="exploreCurated"]/div[1]/div[2]/h2/a').click()
    sleep(3)
    element = driver.find_element(By.XPATH, '//*[@id="ember13"]')
    # Scroll to the element
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    sleep(3)
    element.click()
    seeall = driver.find_element(By.XPATH, '/html/body/div[3]/main/div[2]/section[5]/div[1]/a').get_attribute('href')
    driver.get(seeall)
    sleep(2)

    # Click the button to load reviews
    driver.find_element(By.XPATH,'/html/body/div[3]/main/div[2]/section/div[2]/div[1]/div[2]/blockquote/button').click()

    # Wait for the reviews to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div')))

    # Extract data
    positive_reviews = []
    negative_reviews = []
    neutral_reviews = []

    while True:
        # Get all the review elements
        review_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div')
        date_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div/div/time')
        person_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[1]')

        for review_element, date_element, person_element in zip(review_elements, date_elements, person_elements):
            reviews.append(review_element.text)
            dates.append(date_element.text)
            persons.append(person_element.text)

        # Check if there is a "More" button available
        more_button = driver.find_element(By.CLASS_NAME, '//*[@id="ember50"]/div[2]/blockquote[1]/button')
        if more_button.text == 'more':
            # Click the "More" button to load the next set of reviews
            more_button.click()
            sleep(2)
        for person, date, review in zip(persons, dates, reviews):
            print("Person:", person)
            print("Date:", date)
            print("Review:", review)
            print()
        sleep(2)
        # Close the reviews popup
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/button').click()
        sleep(3)

else:
    driver.get("https://play.google.com/store")

    # Click on the search icon
    search_icon = driver.find_element(By.CSS_SELECTOR, '#kO001e > header > nav > div > div:nth-child(1) > button > i')
    search_icon.click()
    sleep(3)

    # Enter the app name in the search box
    search_box = driver.find_element(By.CSS_SELECTOR, '#kO001e > header > nav > c-wiz > div > div > label > input')
    search_box.send_keys(app_name)
    search_box.send_keys(Keys.RETURN)  # Press Enter key to trigger search
    sleep(8)

    # Wait for the search results to load
    # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@data-uitype="500"]')))

    # Click on the first search result
    search_results = driver.find_elements(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[3]/div/div/c-wiz/c-wiz[1]/c-wiz/section/div/div/a')
    if search_results:
        search_results[0].click()
        sleep(20)
        # Wait for the app page to load
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "UD7Dzf")))

        See_all_reviews = driver.find_element(By.XPATH, "//span[contains(text(),'See all reviews')]")

        # Scroll to the button element using JavaScript
        driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top - window.innerHeight/2);",See_all_reviews)
        sleep(10)
        # Click the button
        See_all_reviews.click()
        sleep(6)

        sort_box = driver.find_element(By.XPATH, '//*[@id="sortBy_1"]/div[2]/span[2]')
        sort_box.click()
        sleep(2)

        Most_Recent = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[5]/div[2]/div/div/div/div/div[2]/div[2]/div/div/span[2]')
        Most_Recent.click()
        sleep(40)


    else:
        print("App not found in the Google Play Store.")
        driver.quit()
        exit()


# Extract and print the reviews and the names of the reviewers
reviews = driver.find_elements(By.CLASS_NAME, 'h3YV2d')
reviewers = driver.find_elements(By.CLASS_NAME, 'X5PpBb')
dates = driver.find_elements(By.CLASS_NAME, 'bp9Aid')
# Initialize empty lists for each sentiment category
positive_reviews = []
negative_reviews = []
neutral_reviews = []

# Check if reviews, reviewers, and dates are found
if reviews and reviewers and dates:
    # Process the reviews and categorize them
    for review, reviewer, date_elem in zip(reviews, reviewers, dates):
        sentiment = analyze_sentiment(review.text)
        if sentiment == 'Positive':
            positive_reviews.append((reviewer.text, review.text, date_elem.text))
        elif sentiment == 'Negative':
            negative_reviews.append((reviewer.text, review.text, date_elem.text))
        else:
            neutral_reviews.append((reviewer.text, review.text, date_elem.text))

    # Print the positive reviews
    print("Positive Reviews:")
    for reviewer, review, date in positive_reviews:
        print(f"{reviewer} on {date}: {review}")
    print()

    # Print the negative reviews
    print("Negative Reviews:")
    for reviewer, review, date in negative_reviews:
        print(f"{reviewer} on {date}: {review}")
    print()

    # Print the neutral reviews
    print("Neutral Reviews:")
    for reviewer, review, date in neutral_reviews:
        print(f"{reviewer} on {date}: {review}")
else:
    print("Reviews not available for the specified app or game.")

# Close the web driver
driver.quit()
