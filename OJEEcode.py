from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Setup Chrome
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://collegedunia.com/college/28535-odisha-university-of-technology-and-research-bhubaneswar")
print("Title:", driver.title)

WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(2)

# Click the "14 Courses" button
try:
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.pointer.text-primary-blue.fs-14.d-flex"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", btn)
    print("✅ Clicked '14 Courses' button.")
except Exception as e:
    print("❌ Could not click '14 Courses' button:", e)
    driver.quit()
    exit()

# Wait for modal content to appear after clicking
try:
    time.sleep(1)  # allow animation to complete
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Computer Science and Engineering')]"))
    )
    print("✅ Modal content appeared.")
except Exception as e:
    print("❌ Modal content not found:", e)
    driver.quit()
    exit()

# Now parse the modal and extract course rows
try:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.select("table.table-new.table-responsive tbody tr")
    if not rows:
        print("⚠️ No '.common-tableRow' elements found. Structure might have changed.")
    output = []
    output.append("Course Name | Fees | Application Date | Cutoff Rank")  # table header
    output.append("-" * 80)

    for row in rows:
        cols = row.select("td")
        if len(cols) >= 4:
           # Extract course name (first <a> tag inside first column)
           course_name = cols[0].find("a").get_text(strip=True) if cols[0].find("a") else cols[0].get_text(strip=True)

           # Extract fees (just the amount + fee type)
           fees = cols[1].get_text(strip=True)

           # Application dates
           date = cols[2].get_text(strip=True)

           # Cutoff rank
           rank = cols[3].get_text(strip=True)

           # Format cleanly
           line = f"{course_name} | {fees} | {date} | {rank}"
           output.append(line)
           output.append("")  # extra line for spacing


    with open("outr_btech_modal_data.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print("✅ Data saved to 'outr_btech_modal_data.txt'.")
except Exception as e:
    print("❌ Failed to extract data from modal:", e)

