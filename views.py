from jinja2 import Environment, PackageLoader, select_autoescape

from common.unicode import emoji


# setting Jinja2-specified params
env = Environment(
    loader=PackageLoader('views'),
    autoescape=select_autoescape()
)
env.trim_blocks = True
env.lstrip_blocks = True


#
# Message templates
#
def hello(username: str):
    """
    Render basic hello template
    """
    template = env.get_template('hello.jinja2')
    return template.render(username=username, emoji=emoji)


def user_connected(message: object):
    """
    Send the info about user connected
    """
    template = env.get_template('user_connected.jinja2')
    return template.render(message=message, emoji=emoji)


def redirect_user_message(message: object, add_id: bool = True,
                          if_data: bool = False):
    """
    Resend user's message to the admins.

    This func by default will add user_id to the message.
    It is used to ensure that user_id will not be lost
    in the chain of the replies.
    """
    user_id_suffix = (
        f'\n{emoji["magniglass"]} <i>id={message.from_user.id}</i>'
    )
    text_template = env.get_template('resend_to_admins.jinja2')
    data_template = env.get_template('resend_object_to_admins.jinja2')
    template = data_template if if_data else text_template
    rendered = template.render(message=message, emoji=emoji)
    if add_id:
        return rendered + user_id_suffix
    return rendered
