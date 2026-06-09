import os
import shutil
import csv


# Create Text File
def create_txt_file():
    try:
        filename = input("Enter TXT file name (example: notes.txt): ")

        with open(filename, "w") as file:
            content = input("Enter file content: ")
            file.write(content)

        print("✅ TXT File created successfully.")

    except Exception as e:
        print("❌ Error:", e)


# Read Text File
def read_txt_file():
    try:
        filename = input("Enter TXT file name to read: ")

        with open(filename, "r") as file:
            data = file.read()

        print("\n----- FILE CONTENT -----")
        print(data)

    except FileNotFoundError:
        print("❌ File not found.")

    except Exception as e:
        print("❌ Error:", e)


# Append Data
def append_data():
    try:
        filename = input("Enter file name: ")

        with open(filename, "a") as file:
            content = input("Enter text to append: ")
            file.write("\n" + content)

        print("✅ Data appended successfully.")

    except Exception as e:
        print("❌ Error:", e)


# Create CSV File
def create_csv_file():
    try:
        filename = input("Enter CSV file name (example: students.csv): ")

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["ID", "Name", "Course"])
            writer.writerow(["101", "Akash", "Python"])
            writer.writerow(["102", "Rahul", "Data Science"])

        print("✅ CSV File created successfully.")

    except Exception as e:
        print("❌ Error:", e)


# Read CSV File
def read_csv_file():
    try:
        filename = input("Enter CSV file name: ")

        with open(filename, "r") as file:
            reader = csv.reader(file)

            print("\n----- CSV CONTENT -----")

            for row in reader:
                print(row)

    except FileNotFoundError:
        print("❌ CSV File not found.")

    except Exception as e:
        print("❌ Error:", e)


# Rename File
def rename_file():
    try:
        old_name = input("Enter current file name: ")
        new_name = input("Enter new file name: ")

        os.rename(old_name, new_name)

        print("✅ File renamed successfully.")

    except FileNotFoundError:
        print("❌ File not found.")

    except Exception as e:
        print("❌ Error:", e)


# Move File
def move_file():
    try:
        source = input("Enter file name to move: ")
        destination = input("Enter destination folder path: ")

        shutil.move(source, destination)

        print("✅ File moved successfully.")

    except FileNotFoundError:
        print("❌ File not found.")

    except Exception as e:
        print("❌ Error:", e)


# Delete File
def delete_file():
    try:
        filename = input("Enter file name to delete: ")

        os.remove(filename)

        print("✅ File deleted successfully.")

    except FileNotFoundError:
        print("❌ File not found.")

    except Exception as e:
        print("❌ Error:", e)


# Main Menu
while True:

    print("\n")
    print("=================================================")
    print(" ALFIDO TECH - TASK 1 FILE MANAGEMENT SYSTEM ")
    print("=================================================")

    print("1. Create TXT File")
    print("2. Read TXT File")
    print("3. Append Data")
    print("4. Create CSV File")
    print("5. Read CSV File")
    print("6. Rename File")
    print("7. Move File")
    print("8. Delete File")
    print("9. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        create_txt_file()

    elif choice == "2":
        read_txt_file()

    elif choice == "3":
        append_data()

    elif choice == "4":
        create_csv_file()

    elif choice == "5":
        read_csv_file()

    elif choice == "6":
        rename_file()

    elif choice == "7":
        move_file()

    elif choice == "8":
        delete_file()

    elif choice == "9":
        print("\n🎉 Thank you for using the system.")
        print("Task 1 Completed Successfully!")
        break

    else:
        print("❌ Invalid Choice. Please try again.")