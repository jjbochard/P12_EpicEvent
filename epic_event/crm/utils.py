from crm.models import Log


def make_log(action, model, field, message, user):
    Log.objects.create(
        action=action, model=model, field=field, message=message, user=user
    )
