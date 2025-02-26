import sys
import os
import gzip
import zipfile

def extract_logs(input_file, target_date, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"output_{target_date}.txt")
    
    with open(output_file, "w") as out_f:
        if input_file.endswith(".zip"):
            with zipfile.ZipFile(input_file, 'r') as zip_ref:
                log_filename = zip_ref.namelist()[0]  # Assuming a single file inside
                with zip_ref.open(log_filename) as log_f:
                    for line in log_f:
                        decoded_line = line.decode("utf-8")
                        if decoded_line.startswith(target_date):
                            out_f.write(decoded_line)
        
        elif input_file.endswith(".gz"):
            with gzip.open(input_file, 'rt', encoding="utf-8") as log_f:
                for line in log_f:
                    if line.startswith(target_date):
                        out_f.write(line)
        
        else:
            with open(input_file, 'r', encoding="utf-8") as log_f:
                for line in log_f:
                    if line.startswith(target_date):
                        out_f.write(line)
    
    print(f"Logs for {target_date} have been saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python src/extract_logs.py <log_file_path> <YYYY-MM-DD>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    date_to_search = sys.argv[2]
    
    if not os.path.exists(log_file_path):
        print("Error: Log file not found.")
        sys.exit(1)
    
    # Process large files efficiently
    try:
        extract_logs(log_file_path,date_to_search)
    except MemoryError:
        print("Error: Insufficient memory to process the file.")
        sys.exit(1)