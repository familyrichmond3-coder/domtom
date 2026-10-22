# ==============================================================
# Web library / Библиотека веб (Flask)
# Install: pip install flask
# ==============================================================
try:
    from flask import Flask, request, jsonify, redirect
    _HAS_FLASK = True
except ImportError:
    _HAS_FLASK = False

_site = None
_routes = []

def route(path, methods=None):
    def deco(fn):
        _routes.append((path, methods, fn))
        return fn
    return deco

def start(name='DoMtor App', host='127.0.0.1', port=5000, debug=True):
    global _site
    if not _HAS_FLASK:
        raise ImportError('Install Flask: pip install flask')
    _site = Flask(name)
    _site.secret_key = 'domtor-secret'
    for path, methods, fn in _routes:
        _site.route(path, methods=methods or ['GET'])(fn)
    _site.run(host=host, port=port, debug=debug)

def html(text):
    return text

def param(name, default=None):
    return request.args.get(name, default) or request.form.get(name, default)

def json_response(data):
    return jsonify(data)

def redirect_to(path):
    return redirect(path)

# Cyrillic aliases
путь         = route
начать       = start
страница     = html
параметр     = param
json_ответ   = json_response
перенаправить = redirect_to