def allowed_image(filename, allowed_extensions):
    if not '.' in filename:
        return False

    ext = filename.rsplit('.', 1)[1]

    if ext in allowed_extensions:
        return True
    else:
        return False