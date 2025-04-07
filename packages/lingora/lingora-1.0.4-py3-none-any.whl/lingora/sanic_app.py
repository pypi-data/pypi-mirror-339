from sanic import Sanic, response, Request
from sanic.response import json as sanic_json
from pathlib import Path
import json
from typing import Dict, Any

def attach_routes(app: Sanic):
    """Attach all routes to the Sanic app"""
    
    def load_json_file(path: str) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json_file(data: dict, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @app.get('/api/index')
    async def get_file_index(request: Request):
        """Return the list of all JSON files in both directories"""
        try:
            source_files = []
            target_files = []
            
            # Get source files
            for file_path in request.app.config.input_path.rglob('*.json'):
                rel_path = str(file_path.relative_to(request.app.config.input_path))
                source_files.append(rel_path)

            # Get target files
            for file_path in request.app.config.output_path.rglob('*.json'):
                rel_path = str(file_path.relative_to(request.app.config.output_path))
                target_files.append(rel_path)
            
            return sanic_json({
                'source': source_files,
                'target': target_files
            })
        except Exception as e:
            return sanic_json({'error': str(e)}, status=500)

    @app.get('/api/file/source/<path:path>')
    async def get_source_file(request: Request, path: str):
        """Get contents of a specific source file"""
        try:
            file_path = request.app.config.input_path / path
            return sanic_json(load_json_file(str(file_path)))
        except Exception as e:
            return sanic_json({'error': str(e)}, status=500)

    @app.get('/api/file/target/<path:path>')
    async def get_target_file(request: Request, path: str):
        """Get contents of a specific target file"""
        try:
            file_path = request.app.config.output_path / path
            return sanic_json(load_json_file(str(file_path)))
        except Exception as e:
            return sanic_json({'error': str(e)}, status=500)

    @app.get('/api/translations')
    async def get_translations(request: Request):
        try:
            source_files = {}
            target_files = {}
            
            # Read source files
            for file_path in request.app.config.input_path.rglob('*.json'):
                rel_path = str(file_path.relative_to(request.app.config.input_path))
                source_files[rel_path] = load_json_file(str(file_path))
            
            # Read target files
            for file_path in request.app.config.output_path.rglob('*.json'):
                rel_path = str(file_path.relative_to(request.app.config.output_path))
                target_files[rel_path] = load_json_file(str(file_path))
            
            return sanic_json({
                'source': source_files,
                'target': target_files
            })
        except Exception as e:
            return sanic_json({'error': str(e)}, status=500)

    @app.post('/api/translations')
    async def update_translation(request: Request):
        try:
            data = request.json
            file_path = request.app.config.output_path / data['file']
            
            # Read existing file
            json_data = load_json_file(str(file_path))
            
            # Update value
            current = json_data
            keys = data['key'].split('.')
            last_key = keys.pop()
            
            for k in keys:
                current = current[k]
            current[last_key] = data['value']
            
            # Save file
            save_json_file(json_data, str(file_path))
            
            return sanic_json({'success': True})
        except Exception as e:
            return sanic_json({'error': str(e)}, status=500)
    @app.get('/reviewer.js')
    async def serve_js(request: Request):
        return await response.file(
            str(request.app.config.reviewer_dir / "reviewer.js"),
            mime_type="application/javascript"
        )

    @app.get('/reviewer.css')
    async def serve_css(request: Request):
        return await response.file(
            str(request.app.config.reviewer_dir / "reviewer.css"),
            mime_type="text/css"
        )
    @app.get('/')
    async def serve_reviewer(request: Request):
        return await response.file(str(request.app.config.reviewer_dir / "reviewer.html"))

def create_app(app_name: str, config: Dict[str, Any]) -> Sanic:
    """Create and configure the Sanic app"""
    app = Sanic(app_name)
    
    # Configure app
    app.config.input_path = config["input_path"]
    app.config.output_path = config["output_path"]
    app.config.reviewer_dir = config["reviewer_dir"]

    # Static files
    app.static('/reviewer', str(config["reviewer_dir"]))

    # Attach routes
    attach_routes(app)

    return app 