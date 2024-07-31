import pandas as pd

def delete_entries_by_column(csv_file_path, column_name):
    """
    Delete the specified column from the CSV file.

    :param csv_file_path: Path to the CSV file
    :param column_name: Name of the column to delete
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Drop the specified column
    if column_name in df.columns:
        df = df.drop(column_name, axis=1)
    else:
        print(f"Column '{column_name}' does not exist in the CSV file.")

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file_path, index=False)

def add_entry(csv_file_path, title, authors, number_of_pages, category, format_):
    """
    Add a new entry to the CSV file with the specified format.

    :param csv_file_path: Path to the CSV file
    :param title: Title of the book
    :param authors: Authors of the book
    :param number_of_pages: Number of pages in the book
    :param category: Category of the book
    :param format_: Format of the book
    """
    # Create a new DataFrame with the new entry
    new_entry = pd.DataFrame([{
        'Title': title,
        'Authors': authors,
        'Number of Pages': number_of_pages,
        'Category': category,
        'Format': format_
    }])

    # Read the existing CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Append the new entry to the DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file_path, index=False)