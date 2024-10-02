import os
from datetime import datetime

# Define the directory where your reports are saved
REPORTS_DIR = "/home/mavindu/Desktop/test/zap-scan-reports/reports/"

# Path to save the main index.html file in the root of your GitHub repository
MAIN_INDEX_FILE_PATH = "/home/mavindu/Desktop/test/zap-scan-reports/index.html"

# Ensure the directory for the main index file exists
if not os.path.exists(os.path.dirname(MAIN_INDEX_FILE_PATH)):
    os.makedirs(os.path.dirname(MAIN_INDEX_FILE_PATH))

# Start creating the main index.html content
main_html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAP Scan Reports</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: white; }
        h1 { text-align: center; color: white; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #333; }
        th { background-color: #333; }
        td { background-color: #222; }
        tr:hover { background-color: #555; }
        a { color: #ffffff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        footer { text-align: center; padding: 10px; background-color: #121212; color: #ffffff; position: fixed; width: 100%; bottom: 0; }
    </style>
</head>
<body>

<h1>OWASP ZAP Scan Reports</h1>

<table>
    <thead>
        <tr>
            <th>Report Folder</th>
            <th>Last Modified</th>
        </tr>
    </thead>
    <tbody>
'''

# Loop through the directories (reports) in the REPORTS_DIR and add them to the main table
for folder_name in sorted(os.listdir(REPORTS_DIR)):
    folder_path = os.path.join(REPORTS_DIR, folder_name)
    
    if os.path.isdir(folder_path):
        # Get the last modified time
        last_modified = datetime.fromtimestamp(os.path.getmtime(folder_path)).strftime('%Y-%m-%d %H:%M:%S')

        # Add a link to the folder itself, to open the folder and display its contents
        main_html_content += f'''
        <tr>
            <td><a href="reports/{folder_name}/index.html">{folder_name}</a></td>
            <td>{last_modified}</td>
        </tr>
        '''

        # Now generate an index.html inside each folder to list all the files within it
        folder_index_path = os.path.join(folder_path, "index.html")
        folder_html_content = '''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Folder: ''' + folder_name + '''</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #121212; color: white; }
                h1 { text-align: center; color: white; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 15px; text-align: left; border-bottom: 1px solid #333; }
                th { background-color: #333; }
                td { background-color: #222; }
                tr:hover { background-color: #555; }
                a { color: #ffffff; text-decoration: none; }
                a:hover { text-decoration: underline; }
                footer { text-align: center; padding: 10px; background-color: #121212; color: #ffffff; position: fixed; width: 100%; bottom: 0; }
            </style>
        </head>
        <body>

        <h1>Files in Folder: ''' + folder_name + '''</h1>

        <table>
            <thead>
                <tr>
                    <th>File Name</th>
                    <th>Last Modified</th>
                </tr>
            </thead>
            <tbody>
        '''
        
        # List all files inside the folder and add them to the folder's index.html
        for file_name in sorted(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                last_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                folder_html_content += f'''
                <tr>
                    <td><a href="{file_name}">{file_name}</a></td>
                    <td>{last_modified}</td>
                </tr>
                '''

        # Finish the folder's index.html content
        folder_html_content += '''
            </tbody>
        </table>

        <footer>
            <a href="../../index.html">Back to Main Reports Page</a>
        </footer>

        </body>
        </html>
        '''
        
        # Save the index.html inside the folder
        with open(folder_index_path, 'w') as folder_file:
            folder_file.write(folder_html_content)

# Finish the main index.html content
main_html_content += '''
    </tbody>
</table>

<footer>
    ZAP Scan Reports | Automated Reports
</footer>

</body>
</html>
'''

# Save the main index.html file
with open(MAIN_INDEX_FILE_PATH, 'w') as main_file:
    main_file.write(main_html_content)

print(f"Main index.html generated successfully at {MAIN_INDEX_FILE_PATH}")

