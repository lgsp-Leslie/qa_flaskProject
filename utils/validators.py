import re

from wtforms import ValidationError


def phone_required(form, field):
    data = field.data
    pattern = r'^1[0-9]{10}$'
    if not re.search(pattern, data):
        raise ValidationError('请输入有效的手机号')
    return field
