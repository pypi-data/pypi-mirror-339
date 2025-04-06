from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import urllib.parse
import cgi
import traceback
import json
import re
import uuid
from typing import Dict, Any, Callable, Optional, Tuple, List, Union

class SimpleWeb:
    def __init__(self, name: str):
        self.name = name
        self.routes = {}
        self.templates = {}
        self.static_dir = "./static"
        self.debug = False
        self.py_handlers = {}  # Store Python event handlers
        self.html_variables = {}  # Store HTML variables
        
    def template(self, name: str, content: str):
        """Register an inline template"""
        self.templates[name] = content
    
    def html_var(self, name: str, content: str):
        """Create a reusable HTML variable"""
        self.html_variables[name] = content
        return self
        
    def get_html_var(self, name: str) -> str:
        """Get the content of an HTML variable"""
        return self.html_variables.get(name, f"HTML variable '{name}' not found")
        
    def render(self, template_name: str, **kwargs) -> str:
        """Render a template with variables"""
        if template_name not in self.templates:
            return f"Template '{template_name}' not found"
            
        content = self.templates[template_name]
        
        # Process Python event handlers
        content = self._process_py_events(content)
        
        # Replace HTML variables
        for var_name, var_content in self.html_variables.items():
            content = content.replace(f"{{{{html.{var_name}}}}}", var_content)
        
        # Replace regular variables
        for key, value in kwargs.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
            
        return content
    
    def _process_py_events(self, content: str) -> str:
        """Process py-event attributes in HTML and convert them to Ajax calls"""
        # Find all py-event attributes in the HTML
        pattern = r'py-(\w+)="([^"]*)"'
        
        def replace_py_event(match):
            event_type = match.group(1)
            handler_code = match.group(2)
            
            # Generate a unique ID for this handler
            handler_id = str(uuid.uuid4())
            
            # Store the Python code to execute when this event occurs
            self.py_handlers[handler_id] = handler_code
            
            # Generate JavaScript event handler that makes an Ajax call to execute the Python code
            return f'''on{event_type}="executePyHandler('{handler_id}', this, event)"'''
            
        # Replace all py-event attributes with corresponding JavaScript event handlers
        processed_content = re.sub(pattern, replace_py_event, content)
        
        # Add the necessary JavaScript to handle Python events
        if len(self.py_handlers) > 0 and "</body>" in processed_content:
            js_code = '''
            <script>
            function executePyHandler(handlerId, element, event) {
                event.preventDefault();
                
                // Get form data if the element is in a form
                let formData = {};
                if (element.form) {
                    const formElements = element.form.elements;
                    for (let i = 0; i < formElements.length; i++) {
                        const el = formElements[i];
                        if (el.name) {
                            formData[el.name] = el.value;
                        }
                    }
                }
                
                // Prepare data to send to server
                const data = {
                    handlerId: handlerId,
                    elementId: element.id || '',
                    elementName: element.name || '',
                    elementValue: element.value || '',
                    formData: formData
                };
                
                // Make Ajax request to execute Python code
                fetch('/execute-py-handler', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.text())
                .then(response => {
                    // Check if response is a command to execute
                    try {
                        const responseObj = JSON.parse(response);
                        if (responseObj.action === 'update') {
                            // Update element content
                            document.querySelector(responseObj.selector).innerHTML = responseObj.content;
                        } else if (responseObj.action === 'redirect') {
                            // Redirect to new page
                            window.location.href = responseObj.url;
                        } else if (responseObj.action === 'setValue') {
                            // Set value of an element
                            document.querySelector(responseObj.selector).value = responseObj.value;
                        } else if (responseObj.action === 'alert') {
                            // Show alert
                            alert(responseObj.message);
                        } else if (responseObj.action === 'eval') {
                            // Execute arbitrary JavaScript (use with caution)
                            eval(responseObj.code);
                        }
                    } catch (e) {
                        // If not JSON, treat as HTML to replace the current page
                        document.open();
                        document.write(response);
                        document.close();
                    }
                })
                .catch(error => {
                    console.error('Error executing Python handler:', error);
                });
                
                return false;
            }
            </script>
            '''
            processed_content = processed_content.replace("</body>", f"{js_code}</body>")
            
        return processed_content
        
    def route(self, path: str, methods: List[str] = None):
        """Decorator to register a route handler with specified HTTP methods"""
        if methods is None:
            methods = ["GET"]
            
        def decorator(handler_func: Callable):
            # Store the route with path and methods
            if path not in self.routes:
                self.routes[path] = {}
                
            for method in methods:
                self.routes[path][method.upper()] = handler_func
                
            return handler_func
        return decorator
    
    def get(self, path: str):
        """Shortcut decorator for GET routes"""
        return self.route(path, methods=["GET"])
    
    def post(self, path: str):
        """Shortcut decorator for POST routes"""
        return self.route(path, methods=["POST"])
    
    def put(self, path: str):
        """Shortcut decorator for PUT routes"""
        return self.route(path, methods=["PUT"])
    
    def delete(self, path: str):
        """Shortcut decorator for DELETE routes"""
        return self.route(path, methods=["DELETE"])
    
    def patch(self, path: str):
        """Shortcut decorator for PATCH routes"""
        return self.route(path, methods=["PATCH"])
    
    def py_response(self, action: str, **kwargs) -> str:
        """Create a response for Python event handlers"""
        response = {"action": action}
        response.update(kwargs)
        return json.dumps(response)
    
    def update_element(self, selector: str, content: str) -> str:
        """Update the content of an element"""
        return self.py_response("update", selector=selector, content=content)
    
    def redirect_client(self, url: str) -> str:
        """Redirect the client to a new URL"""
        return self.py_response("redirect", url=url)
    
    def set_value(self, selector: str, value: str) -> str:
        """Set the value of an input element"""
        return self.py_response("setValue", selector=selector, value=value)
    
    def alert(self, message: str) -> str:
        """Show an alert message"""
        return self.py_response("alert", message=message)
    
    def execute_js(self, code: str) -> str:
        """Execute JavaScript code on the client"""
        return self.py_response("eval", code=code)
        
    def set_static_dir(self, directory: str):
        """Set the directory for static files"""
        self.static_dir = directory
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    def redirect(self, location: str) -> str:
        """Create a redirect response"""
        return f"<!DOCTYPE html><html><head><meta http-equiv='refresh' content='0;url={location}'></head></html>"
    
    def json_response(self, data: Any) -> str:
        """Create a JSON response"""
        return json.dumps(data)
        
    def run(self, host: str = "localhost", port: int = 8000, debug: bool = False):
        """Run the web server"""
        self.debug = debug
        server_address = (host, port)
        
        # Create request handler with access to the app
        app = self
        
        class RequestHandler(BaseHTTPRequestHandler):
            def parse_body(self):
                """Parse request body"""
                content_type = self.headers.get('Content-Type', '')
                
                if not self.headers.get('Content-Length'):
                    return {}
                    
                length = int(self.headers.get('Content-Length', 0))
                if length == 0:
                    return {}
                    
                if 'application/json' in content_type:
                    body_data = self.rfile.read(length).decode('utf-8')
                    return json.loads(body_data)
                elif 'application/x-www-form-urlencoded' in content_type:
                    body_data = self.rfile.read(length).decode('utf-8')
                    return dict(urllib.parse.parse_qsl(body_data))
                elif 'multipart/form-data' in content_type:
                    form = cgi.FieldStorage(
                        fp=self.rfile,
                        headers=self.headers,
                        environ={'REQUEST_METHOD': self.command}
                    )
                    data = {}
                    for field in form.keys():
                        if form[field].filename:
                            # Handle file uploads
                            data[field] = {
                                'filename': form[field].filename,
                                'type': form[field].type,
                                'value': form[field].value
                            }
                        else:
                            data[field] = form[field].value
                    return data
                else:
                    # For other content types, return raw data
                    body_data = self.rfile.read(length)
                    return {'raw': body_data}
                
            def parse_query(self):
                """Parse URL query parameters"""
                parsed_url = urllib.parse.urlparse(self.path)
                return dict(urllib.parse.parse_qsl(parsed_url.query))
                
            def get_clean_path(self):
                """Get path without query parameters"""
                return urllib.parse.urlparse(self.path).path
            
            # Define handlers for all HTTP methods
            def do_GET(self):
                self.handle_request('GET')
                
            def do_POST(self):
                self.handle_request('POST')
                
            def do_PUT(self):
                self.handle_request('PUT')
            
            def do_DELETE(self):
                self.handle_request('DELETE')
                
            def do_PATCH(self):
                self.handle_request('PATCH')
                
            def do_HEAD(self):
                self.handle_request('HEAD')
                
            def do_OPTIONS(self):
                self.handle_request('OPTIONS')
                
            def handle_request(self, method):
                try:
                    path = self.get_clean_path()
                    
                    # Handle static files
                    if path.startswith('/static/'):
                        self.serve_static_file(path[7:])  # Remove '/static/' prefix
                        return
                    
                    # Handle Python event handlers
                    if path == '/execute-py-handler':
                        self.handle_py_event()
                        return
                        
                    # Check if route exists
                    if path in app.routes and method in app.routes[path]:
                        # Prepare request object
                        request = {
                            'method': method,
                            'path': path,
                            'query': self.parse_query(),
                            'headers': {key: value for key, value in self.headers.items()},
                            'body': self.parse_body() if method != 'GET' else {}
                        }
                        
                        # Call route handler
                        response = app.routes[path][method](request)
                        
                        # Send response
                        self.send_response(200)
                        
                        # Determine content type (if response is JSON string, use application/json)
                        content_type = 'text/html'
                        try:
                            json.loads(response)  # Test if response is valid JSON
                            content_type = 'application/json'
                        except (json.JSONDecodeError, TypeError):
                            pass
                            
                        self.send_header('Content-type', content_type)
                        self.end_headers()
                        
                        if isinstance(response, str):
                            self.wfile.write(response.encode())
                        elif isinstance(response, bytes):
                            self.wfile.write(response)
                        else:
                            self.wfile.write(str(response).encode())
                    else:
                        # Check if path exists but method not allowed
                        if path in app.routes:
                            self.send_response(405)  # Method Not Allowed
                            self.send_header('Content-type', 'text/html')
                            self.send_header('Allow', ', '.join(app.routes[path].keys()))
                            self.end_headers()
                            self.wfile.write(b"405 - Method Not Allowed")
                        else:
                            # Route not found
                            self.send_response(404)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(b"404 - Route not found")
                except Exception as e:
                    if app.debug:
                        # Show error details in debug mode
                        self.send_response(500)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        error_msg = f"<h1>500 Server Error</h1><pre>{traceback.format_exc()}</pre>"
                        self.wfile.write(error_msg.encode())
                    else:
                        # Generic error in production
                        self.send_response(500)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b"500 - Server Error")
            
            def handle_py_event(self):
                """Handle Python event execution"""
                try:
                    # Parse request data
                    data = self.parse_body()
                    handler_id = data.get('handlerId')
                    
                    if handler_id in app.py_handlers:
                        # Get the Python code to execute
                        code = app.py_handlers[handler_id]
                        
                        # Create a context with data and helper functions
                        context = {
                            'data': data,
                            'element_id': data.get('elementId'),
                            'element_name': data.get('elementName'),
                            'element_value': data.get('elementValue'),
                            'form_data': data.get('formData', {}),
                            'update_element': app.update_element,
                            'redirect': app.redirect_client,
                            'set_value': app.set_value,
                            'alert': app.alert,
                            'execute_js': app.execute_js,
                            'html_var': app.get_html_var  # Access to HTML variables
                        }
                        
                        # Execute the Python code with the context
                        local_vars = {}
                        exec(f"def handler_func(data, element_id, element_name, element_value, form_data, update_element, redirect, set_value, alert, execute_js, html_var):\n {code}\nresult = handler_func(data, element_id, element_name, element_value, form_data, update_element, redirect, set_value, alert, execute_js, html_var)", {}, local_vars)
                        result = local_vars.get('result', '')
                        
                        # Send the result back to the client
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(str(result).encode())
                    else:
                        # Handler not found
                        self.send_response(404)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b"Handler not found")
                except Exception as e:
                    # Error executing handler
                    self.send_response(500)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    if app.debug:
                        self.wfile.write(f"Error executing handler: {str(e)}\n{traceback.format_exc()}".encode())
                    else:
                        self.wfile.write(b"Error executing handler")
                        
            def serve_static_file(self, file_path):
                """Serve a static file"""
                try:
                    file_path = os.path.join(app.static_dir, file_path)
                    
                    # Basic security check to prevent directory traversal
                    if not os.path.abspath(file_path).startswith(os.path.abspath(app.static_dir)):
                        self.send_response(403)
                        self.end_headers()
                        return
                        
                    if not os.path.exists(file_path):
                        self.send_response(404)
                        self.end_headers()
                        return
                        
                    # Determine content type based on file extension
                    _, ext = os.path.splitext(file_path)
                    content_types = {
                        '.css': 'text/css',
                        '.js': 'application/javascript',
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.png': 'image/png',
                        '.gif': 'image/gif',
                        '.svg': 'image/svg+xml',
                        '.html': 'text/html',
                        '.txt': 'text/plain',
                        '.json': 'application/json',
                        '.pdf': 'application/pdf',
                        '.xml': 'application/xml',
                        '.woff': 'font/woff',
                        '.woff2': 'font/woff2',
                        '.ttf': 'font/ttf',
                        '.eot': 'application/vnd.ms-fontobject',
                        '.otf': 'font/otf',
                        '.mp4': 'video/mp4',
                        '.webm': 'video/webm',
                        '.mp3': 'audio/mpeg',
                        '.wav': 'audio/wav',
                    }
                    content_type = content_types.get(ext.lower(), 'application/octet-stream')
                    
                    # Read and serve the file
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        
                    self.send_response(200)
                    self.send_header('Content-type', content_type)
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    if app.debug:
                        self.wfile.write(str(e).encode())
        
        # Start the server
        print(f"Server started at http://{host}:{port}")
        print(f"Debug mode: {'Enabled' if debug else 'Disabled'}")
        
        if host == "0.0.0.0":
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"Access from other devices on the network at: http://{local_ip}:{port}")
            
        httpd = HTTPServer(server_address, RequestHandler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")