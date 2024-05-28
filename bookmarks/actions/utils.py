import datetime

from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)  # 60s前的时间
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target=target.id)
    if not similar_actions:
        # 如果提供了target参数，那么查询结果将会进一步过滤，只包括那些目标对象是特定目标的动作
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
