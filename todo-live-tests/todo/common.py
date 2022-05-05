def get_object_or_none(Model, obj_id):
    try:
        obj = Model.objects.get(id=obj_id)
        return obj
    except Model.DoesNotExist:
        return None
