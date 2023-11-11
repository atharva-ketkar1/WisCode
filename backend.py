import requests
from bs4 import BeautifulSoup
import csv


class CourseScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape(self):
        scraped_courses = []
        response = requests.get(self.base_url)
        if response.status_code != 200:
            print('Failed to retrieve ' + self.base_url)
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        courses = soup.find_all('div', class_='courseblock')
        print('Found ' + str(len(courses)) + ' courses')
        for course in courses:
            class_name_element = course.select_one('.courseblocktitle .courseblockcode')
            class_name = class_name_element.text.strip() if class_name_element else ""

            credits_element = course.select_one('.courseblockcredits')
            credits = credits_element.text.strip() if credits_element else ""

            prerequisites_element = course.select_one('.courseblockextra .cbextra-data')
            prerequisites = prerequisites_element.text.strip() if prerequisites_element else ""

            print("Class name:", class_name)
            print("Credits:", credits)
            #print("Prerequisites:", prerequisites)   

            scraped_courses.append({
                'class_name': class_name,
                'credits': credits,
                'prerequisites': prerequisites
            })
        self.write_to_csv(scraped_courses)

    def write_to_csv(self, courses):
        with open('courses.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Class Name', 'Credits', 'Prerequisites'])
            for course in courses:
                writer.writerow([course['class_name'], course['credits'], course['prerequisites']])
            print('Wrote ' + str(len(courses)) + ' courses to courses.csv')

if __name__ == "__main__":
    base_url = 'https://guide.wisc.edu/courses/comp_sci/'

    scraper = CourseScraper(base_url)

    scraper.scrape()
