import datetime

class ModelMixin:
    def to_dict(self, exclude=()):
        force_str_types = (datetime.datetime, datetime.date,datetime.time)
        att_dict = {}

        for field in self._meta.fields:
            name = field.attname
            value = getattr(self, field.attname, None)
            if name not in exclude:
                if isinstance(value, force_str_types):
                    value = str(value)
                att_dict[name] = value
        return att_dict

