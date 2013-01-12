pyramid_mustache
================

Extensions for pyramid to use mustache as the rendering engine

In your main of __init__.py:

    config.add_renderer(
        name='.html'
        , factory='pyramid_mustache.MustacheRendererFactory'
    )

In your setup.py's message_extractors:

    ('templates/**.mustache', 'pyramid_mustache.extract_mustache', None),
            
