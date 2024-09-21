import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to convert a single .epub file to .mobi using Calibre's ebook-convert
def convert_epub_to_mobi(epub_path, output_dir):
    try:
        # Get the base name (without extension) of the epub file
        base_name = os.path.splitext(os.path.basename(epub_path))[0]
        # Define the output .mobi file path in the current working directory
        mobi_output_path = os.path.join(output_dir, f"{base_name}.mobi")
        
        # Run the Calibre ebook-convert command with explicit encoding handling
        result = subprocess.run(['ebook-convert', epub_path, mobi_output_path], 
                                capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            return f"Successfully converted: {epub_path} to {mobi_output_path}"
        else:
            return f"Failed to convert: {epub_path}\n{result.stderr}"
    
    except Exception as e:
        return f"Error converting {epub_path}: {str(e)}"

# Function to collect all .epub files in a directory and its subdirectories
def collect_epubs(directory):
    epub_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.epub'):
                epub_files.append(os.path.join(root, file))
    return epub_files

# Function to convert multiple epub files using a thread pool
def walk_and_convert_parallel(directory, output_dir, max_workers=10):
    epub_files = collect_epubs(directory)

    # Use ThreadPoolExecutor to convert files in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_epub = {executor.submit(convert_epub_to_mobi, epub, output_dir): epub for epub in epub_files}
        
        for future in as_completed(future_to_epub):
            epub_path = future_to_epub[future]
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"Error in converting {epub_path}: {str(e)}")

if __name__ == "__main__":
    # Define the directory to search for .epub files
    search_directory = 'G:\\My Drive\\Books\\ספרי קריאה\\ספרים בעברית'  # Replace with the path where your .epub files are located
    # The current working directory where the .mobi files will be saved
    output_directory = os.getcwd()

    # Convert epub files in parallel using up to 10 threads
    walk_and_convert_parallel(search_directory, output_directory, max_workers=10)
    print("Conversion process completed.")
