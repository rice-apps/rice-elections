from gaesessions import SessionMiddleware

# suggestion: generate your own random key using os.urandom(64)
# WARNING: Make sure you run os.urandom(64) OFFLINE and copy/paste the output to
# this file.  If you use os.urandom() to *dynamically* generate your key at
# runtime then any existing sessions will become junk every time you start,
# deploy, or update your app!
COOKIE_KEY = '\x98;\x1eq\xd0\r\x0e\xe4G\xabZ\xf7\x8f:R\x15\xd8\xb9\x8c\xf7\x0c\xa9\xeb\xd6\x8a55\xdb\xbf\xc3Nd\xf2k\xb7;<\x14\x06g\xa7\xb9\xd5\xf2@`D\x1fD\xb1sO\x9a|-\xe2\x15\xb4l\x1c\x17\xcd#3'

def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
    app = recording.appstats_wsgi_middleware(app)
    return app
