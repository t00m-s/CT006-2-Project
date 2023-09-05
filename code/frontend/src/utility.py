from datetime import datetime

from flask import render_template


def render_with_lib(page, **kwargs):
    kwargs['boostrap_js'] = [
        '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>'
    ]

    kwargs['boostrap_css'] = [
        '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">'
    ]

    kwargs['jquery_js'] = [
        '<script src="https://code.jquery.com/jquery-3.6.4.min.js" integrity="sha256-oP6HI9z1XaZNBrJURtCoUT5SUnxFr8s3BzRl+cbzUq8=" crossorigin="anonymous"></script>'
    ]

    kwargs['online_lib_css'] = [
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/toastify-js/1.6.1/toastify.min.css" integrity="sha512-UiKdzM5DL+I+2YFxK+7TDedVyVm7HMp/bN85NeWMJNYortoll+Nd6PU9ZDrZiaOsdarOyk9egQm6LOJZi36L2g==" crossorigin="anonymous" referrerpolicy="no-referrer" />'
    ]

    kwargs['js_libraries'] = [
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/toastify-js/1.6.1/toastify.min.js" integrity="sha512-79j1YQOJuI8mLseq9icSQKT6bLlLtWknKwj1OpJZMdPt2pFBry3vQTt+NZuJw7NSd1pHhZlu0s12Ngqfa371EA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'
    ]

    kwargs['icons_css'] = [
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />',
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css" />'
    ]
    kwargs['logo'] = '/frontend/static/img/logo_unive_white.png'

    kwargs['download_icon'] = '/frontend/static/img/pdf.png'

    kwargs['placeholder'] = 'frontend/static/img/placeholder_unive.jpg'

    if kwargs.get('custom_css') is None:
        kwargs['custom_css'] = [
            '/frontend/static/css/style.css'
        ]
    else:
        kwargs['custom_css'] = ['/frontend/static/css/style.css'] + ([
                                                                         kwargs['custom_css']] if not isinstance(
            kwargs['custom_css'], list) else kwargs['custom_css'])

    if kwargs.get('custom_javascript') is None:
        kwargs['custom_javascript'] = [
            '/frontend/static/js/scripts.js'
        ]
    else:
        kwargs['custom_javascript'] = ['/frontend/static/js/scripts.js'] + (
            [kwargs['custom_javascript']] if not isinstance(kwargs['custom_javascript'], list) else kwargs[
                'custom_javascript'])

    kwargs['year'] = datetime.today().year

    # TODO FARE LO STESSO PER QUANTO RIGUARDA GLI STATI DEL PROGETTO, PER FARLO: PER OGNI PROGETTO PRENDERE L'ULTIMO STATO
    # TODO: Deve esserci un modo pythonesco per fare tipo set(kwargs) senza 
    #       cicli
    return render_template(page, **kwargs)
