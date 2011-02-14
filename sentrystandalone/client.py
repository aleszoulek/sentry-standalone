import traceback

from sentrystandalone.helpers import get_frames, send



def report(sentry_url, sentry_key, exc_info, view, url):
    exc_class, exception, tb = exc_info
    frames = get_frames(tb)
    data = {
        'class_name': exc_class.__name__,
        'data': {
            '__sentry__': {
                'exc': [
                    exc_class.__name__,
                    (unicode(exception),),
                    frames
                ]
            },
         },
        'level': 40,
        'message': unicode(exception),
        'server_name': 'bebe',
        'site': u'example.com',
        'traceback': traceback.format_exc(exc_info),
        'url': url,
        'view': view,
    }
    send(
        sentry_url,
        data,
        sentry_key,
    )

