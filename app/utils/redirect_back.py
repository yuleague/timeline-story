# app.utils.redirect_back

from flask import request, url_for, redirect

def redirect_back(default='home', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def errorhandler(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'invalid request'})
        response.status_code = 400 or 404
        return response
    return redirect(render_template('404.html'))

def safe_heathcheck():
    return jsonify({'status': 'ok'}), 200