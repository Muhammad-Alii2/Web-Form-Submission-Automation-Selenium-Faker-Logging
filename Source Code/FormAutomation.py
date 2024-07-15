import csv
import logging
import os
import random
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize Faker for generating fake data
fake = Faker()

# Configure logging to track form submissions
logging.basicConfig(
    filename='../Output Files/form_submission.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

# Define input and output CSV file paths
input_csv_file = r'../Input Files/form_data.csv'
output_csv_file = r'../Output Files/form_data.csv'

# Lists of subjects, hobbies, and picture paths
subjects = ["Maths", "English", "History", "Economics", "Physics",
            "Chemistry", "Biology", "Computer Science", "Arts", "Commerce"]

hobbies = ["Sports", "Reading", "Music"]

picture_paths = [r'D:\example\test1.jpg',
                 r'D:\example\test2.jpg',
                 r'D:\example\test3.jpg']

# Dictionary mapping states to their cities
states_cities = {
    "NCR": ["Delhi", "Gurgaon", "Noida"],
    "Uttar Pradesh": ["Agra", "Lucknow", "Merrut"],
    "Haryana": ["Karnal", "Panipat"],
    "Rajasthan": ["Jaipur", "Jaiselmer"]
}


def saveToCsv(data, file_path=output_csv_file):
    # Check if the output CSV file exists
    file_exists = os.path.isfile(file_path)
    # Open the CSV file in append mode
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["First Name", "Last Name", "Email", "Gender",
                                                  "Phone Number", "Birth Date", "Subjects",
                                                  "Hobbies", "Picture", "Address", "State", "City"])
        # Write the header if the file is being created
        if not file_exists:
            writer.writeheader()
        # Write the data to the CSV
        writer.writerow(data)

def generateRandomNumber():
    # Generate a random US phone number
    area_code = random.randint(100, 999)
    central_office_code = random.randint(100, 999)
    line_number = random.randint(1000, 9999)
    return int(f"1{area_code}{central_office_code}{line_number}")


def autoFormSubmission(driver, num_forms):
    global Email

    for _ in range(num_forms):
        try:
            # Navigate to the form page
            driver.get("https://demoqa.com/automation-practice-form")

            # Generate random data using Faker
            First_Name = fake.first_name()
            Last_Name = fake.last_name()
            Email = fake.email()
            driver.find_element(By.ID, 'firstName').send_keys(First_Name)
            driver.find_element(By.ID, 'lastName').send_keys(Last_Name)
            driver.find_element(By.ID, 'userEmail').send_keys(Email)

            # Randomly select gender
            Gender = random.choice(["Male", "Female", "Other"])
            gender_id = None
            if Gender.lower() == 'male':
                gender_id = 'gender-radio-1'
            elif Gender.lower() == 'female':
                gender_id = 'gender-radio-2'
            elif Gender.lower() == 'other':
                gender_id = 'gender-radio-3'
            driver.find_element(By.XPATH, f"//label[@for='{gender_id}']").click()

            # Generate random phone number
            Phone_Number = generateRandomNumber()
            driver.find_element(By.ID, 'userNumber').send_keys(Phone_Number)

            # Fill in the date of birth
            date_input = driver.find_element(By.ID, 'dateOfBirthInput')
            driver.execute_script("arguments[0].scrollIntoView();", date_input)
            date_input.click()
            Birth_Date = fake.date_of_birth(minimum_age=18, maximum_age=95)
            year, month, day = Birth_Date.isoformat().split('-')
            year = int(year)
            month = int(month.lstrip('0')) - 1  # Adjust for zero-indexed months
            day = int(day.lstrip('0'))
            driver.find_element(By.XPATH,
                            f"//select[@class='react-datepicker__year-select']/option[@value='{year}']").click()
            driver.find_element(By.XPATH,
                            f"//select[@class='react-datepicker__month-select']/option[@value='{month}']").click()
            driver.find_element(By.XPATH,
                                f"//div[contains(@class, 'react-datepicker__day') and text()='{day}']").click()

            # Select favorite subjects
            driver.find_element(By.ID, 'subjectsContainer').click()
            Favorite_Subjects = random.sample(subjects, random.randint(1, 5))
            subject_field = driver.find_element(By.ID, 'subjectsInput')
            for subject in Favorite_Subjects:
                subject_field.send_keys(subject)
                subject_field.send_keys(Keys.RETURN)

            # Select hobbies
            Hobbies = random.sample(hobbies, random.randint(1, 3))
            if 'Sports' in Hobbies:
                driver.find_element(By.XPATH, f"//label[@for='hobbies-checkbox-1']").click()
            if 'Reading' in Hobbies:
                driver.find_element(By.XPATH, f"//label[@for='hobbies-checkbox-2']").click()
            if 'Music' in Hobbies:
                driver.find_element(By.XPATH, f"//label[@for='hobbies-checkbox-3']").click()

            # Upload a picture
            Picture_Path = random.choice(picture_paths)
            driver.find_element(By.ID, 'uploadPicture').send_keys(Picture_Path)

            # Fill in the address
            Address = fake.address()
            driver.find_element(By.ID, 'currentAddress').send_keys(Address)

            # Select a state and city
            State = random.choice(list(states_cities.keys()))
            driver.find_element(By.ID, 'state').click()
            state_field = driver.find_element(By.ID, 'react-select-3-input')
            state_field.send_keys(State)
            state_field.send_keys(Keys.RETURN)

            City = random.choice(states_cities[State])
            driver.find_element(By.ID, 'city').click()
            city_field = driver.find_element(By.ID, 'react-select-4-input')
            city_field.send_keys(City)
            city_field.send_keys(Keys.RETURN)

            # Submit the form
            submit_button = driver.find_element(By.ID, 'submit')
            driver.execute_script("arguments[0].scrollIntoView();", submit_button)
            submit_button.click()
            time.sleep(5)  # Wait for submission to complete

            # Prepare data for saving to CSV
            data = {
                "First Name": First_Name,
                "Last Name": Last_Name,
                "Email": Email,
                "Gender": Gender,
                "Phone Number": Phone_Number,
                "Birth Date": Birth_Date,
                "Subjects": ", ".join(Favorite_Subjects),
                "Hobbies": ", ".join(Hobbies),
                "Picture": Picture_Path,
                "Address": Address,
                "State": State,
                "City": City
            }

            # Save the submitted data to the output CSV
            saveToCsv(data)

            logging.info(f"Form submitted successfully for {Email}")
        except Exception as e:
            print(e)
            logging.error(f"Error submitting form for {Email}: {e}")


def read_csv(file_path):
    # Read data from the input CSV file
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def csvFormSubmission(driver, data):
    try:
        # Open the web form page
        driver.get("https://demoqa.com/automation-practice-form")

        # Fill in the text fields using data from the CSV
        driver.find_element(By.ID, 'firstName').send_keys(data['First Name'])
        driver.find_element(By.ID, 'lastName').send_keys(data['Last Name'])
        driver.find_element(By.ID, 'userEmail').send_keys(data['Email'])

        # Select gender radio button based on the data
        gender_value = data['Gender']
        gender_id = None
        if gender_value.lower() == 'male':
            gender_id = 'gender-radio-1'
        elif gender_value.lower() == 'female':
            gender_id = 'gender-radio-2'
        elif gender_value.lower() == 'other':
            gender_id = 'gender-radio-3'
        driver.find_element(By.XPATH, f"//label[@for='{gender_id}']").click()

        # Fill in the phone number
        driver.find_element(By.ID, 'userNumber').send_keys(data['Phone Number'])

        # Fill in the date of birth
        date_input = driver.find_element(By.ID, 'dateOfBirthInput')
        driver.execute_script("arguments[0].scrollIntoView();", date_input)
        date_input.click()
        day, month, year = data['Birth Date'].split("/")
        day = int(day.lstrip('0'))
        month = int(month.lstrip('0')) - 1  # Adjust for zero-indexed months
        driver.find_element(By.XPATH,
                        f"//select[@class='react-datepicker__year-select']/option[@value='{year}']").click()
        driver.find_element(By.XPATH,
                        f"//select[@class='react-datepicker__month-select']/option[@value='{month}']").click()
        driver.find_element(By.XPATH,
                            f"//div[contains(@class, 'react-datepicker__day') and text()='{day}']").click()

        # Fill in the subjects multi-field
        driver.find_element(By.ID, 'subjectsContainer').click()
        subject_list = [subject.strip() for subject in data['Subjects'].split(",")]
        subject_field = driver.find_element(By.ID, 'subjectsInput')
        for subject in subject_list:
            subject_field.send_keys(subject)
            subject_field.send_keys(Keys.RETURN)

        # Checkmark the hobbies checkboxes
        hobby_list = [hobby.strip() for hobby in data['Hobbies'].split(",")]
        if 'Sports' in hobby_list:
            driver.find_element(By.XPATH, f"//label[@for='hobbies-checkbox-1']").click()
        if 'Reading' in hobby_list:
            driver.find_element(By.XPATH, f"//label[@for='hobbies-checkbox-2']").click()
        if 'Music' in hobby_list:
            driver.find_element(By.XPATH, f"//label[@for='hobbies-checkbox-3']").click()

        # Upload a picture
        driver.find_element(By.ID, 'uploadPicture').send_keys(fr"{data['Picture']}")

        # Fill in the address field
        driver.find_element(By.ID, 'currentAddress').send_keys(data['Address'])

        # Select from the state dropdown
        driver.find_element(By.ID, 'state').click()
        state_field = driver.find_element(By.ID, 'react-select-3-input')
        state_field.send_keys(data['State'])
        state_field.send_keys(Keys.RETURN)

        # Select from the city dropdown
        driver.find_element(By.ID, 'city').click()
        city_field = driver.find_element(By.ID, 'react-select-4-input')
        city_field.send_keys(data['City'])
        city_field.send_keys(Keys.RETURN)

        # Click the submit button
        submit_button = driver.find_element(By.ID, 'submit')
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()
        time.sleep(5)  # Wait for submission to complete

        logging.info(f"Form submitted successfully for {data['Email']}")
    except Exception as e:
        print(e)
        logging.error(f"Error submitting form for {data['Email']}: {e}")

# Prompt user for their choice of form submission method
user_choice = input("Do you want to fill the form using CSV (y/n)? ").strip().lower()

if user_choice == 'y':
    # If user chooses CSV, check if the file exists and read data
    if os.path.exists(input_csv_file):
        data_list = read_csv(input_csv_file)
        driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
        for data in data_list:
            csvFormSubmission(driver, data)  # Submit each form entry from CSV
        driver.quit()  # Close the browser after submission
    else:
        print("CSV file does not exist.")
else:
    # If user chooses to auto-generate forms, ask how many to generate
    num_forms = int(input("How many forms do you want to auto-generate? "))
    driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
    autoFormSubmission(driver, num_forms)  # Auto-generate and submit forms
    driver.quit()  # Close the browser after submission
