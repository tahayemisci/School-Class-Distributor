import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import random
import xlsxwriter
import tkinter as tk
from tkinter import filedialog, messagebox
import os


# Function to load data from an Excel file
def load_data(file_path):
    students_df = pd.read_excel(file_path)
    return students_df


# Function to sort students by grade
def sort_students(students_df):
    return students_df.sort_values(by='Grade', ascending=False).reset_index(drop=True)


# Function to calculate mean and standard deviation
def calculate_statistics(students_df):
    mean_grade = students_df['Grade'].mean()
    std_dev = students_df['Grade'].std()
    return mean_grade, std_dev


# Function to generate subgroups based on grade ranges
def get_grade_group(grade, mean_grade, std_dev):
    if grade < mean_grade - std_dev:
        return 'E'
    elif mean_grade - std_dev <= grade < mean_grade - std_dev / 2:
        return 'D'
    elif mean_grade - std_dev / 2 <= grade < mean_grade + std_dev / 2:
        return 'C'
    elif mean_grade + std_dev / 2 <= grade < mean_grade + std_dev:
        return 'B'
    else:
        return 'A'


# Function to process data separately for foreign and local students
def process_students(students_df, mean_grade, std_dev):
    students_df['Grade Group'] = students_df['Grade'].apply(lambda grade: get_grade_group(grade, mean_grade, std_dev))
    foreign_students = students_df[students_df['Nationality'] == 'Yabancı']
    local_students = students_df[students_df['Nationality'] == 'Yerli']
    return foreign_students, local_students


# Function to distribute students to balance foreign students first, then genders
def balanced_distribute_students(foreign_students, local_students, num_classes):
    class_names = [f'{string.ascii_uppercase[i]} Sınıfı' for i in range(num_classes)]
    classes = {class_name: [] for class_name in class_names}
    class_counters = {class_name: {'Erkek': 0, 'Kız': 0, 'Yabancı': 0, 'Total': 0} for class_name in class_names}

    # Distribute foreign students first
    for i, student in foreign_students.iterrows():
        chosen_class = min(class_names, key=lambda x: class_counters[x]['Yabancı'])
        classes[chosen_class].append(student.to_dict())
        class_counters[chosen_class]['Yabancı'] += 1
        class_counters[chosen_class][student['Gender']] += 1
        class_counters[chosen_class]['Total'] += 1

    # Distribute local students
    for i, student in local_students.iterrows():
        chosen_class = min(class_names,
                           key=lambda x: (class_counters[x]['Total'], class_counters[x][student['Gender']]))
        classes[chosen_class].append(student.to_dict())
        class_counters[chosen_class][student['Gender']] += 1
        class_counters[chosen_class]['Total'] += 1

    # Sort students within each class by grade
    for class_name in classes:
        classes[class_name] = sorted(classes[class_name], key=lambda x: x['Grade'], reverse=True)

    return classes


# Function to write class data and summary to a sheet
def write_class_sheet(writer, class_name, class_df):
    # Calculate summary information
    class_size = class_df.shape[0]
    num_foreign = class_df[class_df['Nationality'] == 'Yabancı'].shape[0]
    num_male = class_df[class_df['Gender'] == 'Erkek'].shape[0]
    num_female = class_df[class_df['Gender'] == 'Kız'].shape[0]
    grade_distribution = class_df['Grade'].describe()

    # Localized column names
    localized_columns = {
        'First Name': 'İsim',
        'Last Name': 'Soyisim',
        'Full Name': 'Tam İsim',
        'Nationality': 'Uyruk',
        'Gender': 'Cinsiyet',
        'Grade': 'Not',
        'Grade Group': 'Not Grubu'
    }
    class_df.rename(columns=localized_columns, inplace=True)

    # Write class data to sheet
    class_df.to_excel(writer, sheet_name=class_name, index=False, startrow=0)

    # Write summary information to the same sheet
    summary_data = {
        'Sınıf Büyüklüğü': [class_size],
        'Yabancı Öğrenciler': [num_foreign],
        'Erkek Öğrenciler': [num_male],
        'Kız Öğrenciler': [num_female],
        'Not Dağılımı': [
            f"Ortalama: {grade_distribution['mean']:.2f}, "
            f"Std: {grade_distribution['std']:.2f}, "
            f"Min: {grade_distribution['min']:.2f}, "
            f"25%: {grade_distribution['25%']:.2f}, "
            f"50%: {grade_distribution['50%']:.2f}, "
            f"75%: {grade_distribution['75%']:.2f}, "
            f"Maks: {grade_distribution['max']:.2f}"
        ]
    }

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name=class_name, index=False, startrow=class_df.shape[0] + 2)

    # Add pie chart to the sheet using the summary table
    workbook = writer.book
    worksheet = writer.sheets[class_name]

    # Create summary table for grade groups
    grade_groups = class_df['Not Grubu'].value_counts().sort_index()
    start_row = class_df.shape[0] + 5

    worksheet.write(start_row, 0, 'Not Grubu')
    worksheet.write(start_row, 1, 'Sayısı')

    for i, (group, count) in enumerate(grade_groups.items()):
        worksheet.write(start_row + i + 1, 0, group)
        worksheet.write(start_row + i + 1, 1, count)

    chart = workbook.add_chart({'type': 'pie'})

    chart.add_series({
        'categories': [class_name, start_row + 1, 0, start_row + len(grade_groups), 0],
        'values': [class_name, start_row + 1, 1, start_row + len(grade_groups), 1],
        'data_labels': {'percentage': True},
    })

    chart.set_title({'name': 'Not Dağılımı'})

    worksheet.insert_chart(f'I{class_df.shape[0] + 4}', chart)

    # Auto-fit columns
    for column in class_df:
        column_width = max(class_df[column].astype(str).map(len).max(), len(column)) + 2
        col_idx = class_df.columns.get_loc(column)
        worksheet.set_column(col_idx, col_idx, column_width)


# Function to save the final Excel file
def save_to_excel(balanced_classes, students_df, output_file_path):
    writer = pd.ExcelWriter(output_file_path, engine='xlsxwriter')

    # Write each class to a separate sheet and add summary information
    for class_name in balanced_classes:
        class_df = pd.DataFrame(balanced_classes[class_name])
        write_class_sheet(writer, class_name, class_df)

    # Write all students' information and summary to a separate sheet
    write_class_sheet(writer, 'Tüm Öğrenciler', students_df)

    # Save the final Excel file properly
    writer.close()

    messagebox.showinfo("Başarılı", f'Sınıf atamaları {output_file_path} dosyasına kaydedildi.')


# Function to handle the Generate button click
def generate_classes():
    # Açıklama: Bu düğmeye tıklayarak veri yükleyebilir ve sınıf atamalarını oluşturabilirsiniz
    file_path = student_file_path.get()
    if not file_path:
        messagebox.showerror("Hata", "Öğrenci bilgilerini içeren Excel dosyasını seçin.")
        return

    students_df = load_data(file_path)
    students_df = sort_students(students_df)
    mean_grade, std_dev = calculate_statistics(students_df)
    foreign_students, local_students = process_students(students_df, mean_grade, std_dev)

    try:
        num_classes = int(num_classes_entry.get())
    except ValueError:
        messagebox.showerror("Hata", "Geçerli bir sınıf sayısı giriniz.")
        return

    balanced_classes = balanced_distribute_students(foreign_students, local_students, num_classes)

    output_file_path = new_excel_file_name.get()
    if not output_file_path.endswith('.xlsx'):
        output_file_path += '.xlsx'

    # Use a temporary directory if the output path is not specified
    if not os.path.isabs(output_file_path):
        output_file_path = os.path.join(os.getcwd(), output_file_path)

    save_to_excel(balanced_classes, students_df, output_file_path)


# Function to select the student information file
def select_student_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel dosyaları", "*.xlsx")])
    student_file_path.set(file_path)


# Ana pencereyi oluştur
root = tk.Tk()
root.title("Sınıf Ataması")

# Öğrenci bilgilerini içeren dosyayı seçmek için buton ve giriş alanı
tk.Label(root, text="Öğrenci Bilgileri Dosyası:").grid(row=0, column=0, padx=10, pady=10)
student_file_path = tk.StringVar()
tk.Entry(root, textvariable=student_file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Dosya Seç", command=select_student_file).grid(row=0, column=2, padx=10, pady=10)

# Sınıf sayısını girmek için giriş alanı
tk.Label(root, text="Kaç sınıf oluşturulacak?:").grid(row=1, column=0, padx=10, pady=10)
num_classes_entry = tk.Entry(root)
num_classes_entry.grid(row=1, column=1, padx=10, pady=10)

# Yeni Excel dosyasının adını girmek için giriş alanı
tk.Label(root, text="Yeni Excel Dosya Adı:").grid(row=2, column=0, padx=10, pady=10)
new_excel_file_name = tk.Entry(root)
new_excel_file_name.grid(row=2, column=1, padx=10, pady=10)

# Açıklama: Bu düğmeye tıklayarak veri yükleyebilir ve sınıf atamalarını oluşturabilirsiniz
generate_button = tk.Button(root, text="Sınıfları Oluştur", command=generate_classes)
generate_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# GUI olay döngüsünü çalıştır
root.mainloop()

