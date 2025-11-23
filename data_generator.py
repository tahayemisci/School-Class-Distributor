import pandas as pd
import numpy as np
import random

# Constants
NUM_STUDENTS = 500
MALE_FIRST_NAMES = ['Murat', 'Mehmet', 'Burak', 'Taha', 'Kerem', 'Alper', 'Mustafa', 'Mert', 'Can', 'Samet', 'Selçuk',
                    'Arda', 'Fatih', 'Yiğit', 'Efe', 'Ege', 'Enes', 'Umut', 'Enis', 'Said', 'Faik', 'Okan', 'Barış',
                    'Fuat', 'Ahmet']
FEMALE_FIRST_NAMES = ['Zeynep', 'Selin', 'Ece', 'Eslem', 'Hilal', 'Naz', 'Ceren', 'Sude', 'Yağmur', 'Ala', 'Pelin',
                      'Serra', 'Aya', 'Zülal', 'Sevde', 'Doğa', 'Hatice', 'Fatma', 'Ayşe', 'Hayriye', 'Berna', 'İrem',
                      'Tuğçe', 'Duygu', 'Esra']
LAST_NAMES = ['Erdoğan', 'Küçük', 'Demir', 'Altay', 'Gitsin', 'Dursun', 'Yemişçi', 'Alemdar', 'Çakır', 'Deniz',
              'Öztürk', 'Dinç', 'Tunç', 'Odabaşı', 'Aktürk', 'Çalhanoğlu', 'Güler', 'Buruk', 'Terim', 'Yılmaz']
NATIONALITIES = ['Yerli', 'Yabancı']
GENDERS = ['Erkek', 'Kız']
MEAN_GRADE = 75
STD_DEV_GRADE = 15


# Function to generate random student data
def generate_random_students(num_students):
    students = []
    num_foreign_students = random.randint(int(num_students * 0.1), int(num_students * 0.2))
    foreign_indices = random.sample(range(num_students), num_foreign_students)

    for i in range(num_students):
        gender = random.choice(GENDERS)
        if gender == 'Erkek':
            first_name = random.choice(MALE_FIRST_NAMES)
        else:
            first_name = random.choice(FEMALE_FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f'{first_name} {last_name}'
        nationality = 'Yabancı' if i in foreign_indices else 'Yerli'
        grade = round(np.random.normal(MEAN_GRADE, STD_DEV_GRADE), 2)
        grade = max(50, min(100, grade))  # Ensure grade is between 50 and 100
        student = {
            'First Name': first_name,
            'Last Name': last_name,
            'Full Name': full_name,
            'Nationality': nationality,
            'Gender': gender,
            'Grade': grade
        }
        students.append(student)
    return students


# Generate the student data
student_data = generate_random_students(NUM_STUDENTS)

# Convert to DataFrame
students_df = pd.DataFrame(student_data)

# Save to Excel
output_file_path = 'Örnek_Öğrenci_Bilgileri-1.xlsx'  # Changed file name to avoid conflicts
students_df.to_excel(output_file_path, index=False)

print(f'Random student data has been saved to {output_file_path}')


