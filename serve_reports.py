import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Define the directory you want to serve, in this case, the 'reports' folder
REPORTS_DIR = "/home/mavindu/Desktop/test/zap-scan-reports/reports/"

class CustomHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """Override the default to serve files from the reports directory"""
        path = path.lstrip('/')
        return os.path.join(REPORTS_DIR, path)

    def list_directory(self, path):
        """Serve a directory listing."""
        try:
            list_dir = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        list_dir.sort(key=lambda a: a.lower())

        r = []
        displaypath = os.path.basename(path)
        r.append(f'<html><head><title>Directory listing for {displaypath}</title></head>')
        r.append('''
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
        </style>''')
        r.append('<body><h1>ZAP Scan Reports</h1>')
        r.append('<table><tr><th>File Name</th><th>Last Modified</th></tr>')

        for name in list_dir:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + '/'
                linkname = name + '/'
            mod_time = self.date_time_string(os.path.getmtime(fullname))
            r.append(f'<tr><td><a href="{linkname}">{displayname}</a></td><td>{mod_time}</td></tr>')

        r.append('</table></body></html>\n')
        encoded = '\n'.join(r).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        return None

def run(server_class=HTTPServer, handler_class=CustomHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print(f"Serving reports from {REPORTS_DIR} on port 8000...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()

