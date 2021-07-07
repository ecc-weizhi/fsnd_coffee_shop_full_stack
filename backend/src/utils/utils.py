def check_fields_exist(request_json, expected_fields):
    missing_fields = []
    for field in expected_fields:
        value = request_json.get(field, None)
        if value is None:
            missing_fields.append(field)

    return missing_fields