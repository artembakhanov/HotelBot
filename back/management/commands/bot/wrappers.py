from back.models import User


def save_user(function):
    def wrapper(m, *args, **kwargs):
        user = User.objects.get_or_create(
            telegram_id=m.chat.id,
            defaults={"first_name": m.from_user.first_name, "last_name": m.from_user.last_name,
                      "username": m.from_user.username}
        )
        return function(m, user, *args, **kwargs)

    return wrapper
