import logging
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp']
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_avatar_image(avatar_file, username='Unknown'):
    """
    Валидация файла аватарки
    Возвращает (is_valid, error_message)
    """
    if not avatar_file:
        return True, None

    # Проверяем content-type
    file_content_type = avatar_file.content_type

    if not file_content_type.startswith('image/'):
        # ❌ Текстовый файл или другой не-изображение
        logger.error(
            f"User {username} attempted to upload non-image file: "
            f"filename={avatar_file.name}, "
            f"content_type={file_content_type}, "
            f"size={avatar_file.size} bytes",
            exc_info=True
        )
        return False, f'Можно загружать только изображения! Вы попытались загрузить файл типа {file_content_type}'

    # Проверяем расширение
    file_extension = avatar_file.name.split('.')[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        logger.warning(
            f"User {username} attempted to upload unsupported image type: "
            f"{file_extension}, filename: {avatar_file.name}"
        )
        return False, f'Неподдерживаемый формат: .{file_extension}. Разрешенные форматы: {", ".join(ALLOWED_EXTENSIONS)}'

    # Проверяем размер
    if avatar_file.size > MAX_AVATAR_SIZE:
        logger.warning(
            f"User {username} attempted to upload oversized avatar: "
            f"{avatar_file.size} bytes (max: {MAX_AVATAR_SIZE}), filename: {avatar_file.name}"
        )
        size_mb = avatar_file.size / (1024 * 1024)
        max_mb = MAX_AVATAR_SIZE / (1024 * 1024)
        return False, f'Файл слишком большой ({size_mb:.2f} MB). Максимальный размер: {max_mb:.0f} MB'

    # ✅ Всё хорошо
    logger.info(
        f"User {username} uploaded valid avatar: "
        f"filename={avatar_file.name}, "
        f"type={file_content_type}, "
        f"size={avatar_file.size} bytes"
    )
    return True, None