import os
from typing import TypeVar, Callable
from django.conf import settings

RT = TypeVar('RT')


def remove_image_after_test(images: list) -> Callable[
        [Callable[..., RT]],
        Callable[..., RT]
]:
    """удаление изображений после теста"""
    def first_wrapper(method: Callable[..., RT]) -> Callable[..., RT]:
        def second_wrapper(self) -> RT:
            try:
                method(self)
            finally:
                for image in images:
                    if os.path.exists(
                            settings.MEDIA_ROOT + '/' +
                            settings.IMAGE_UPLOAD_FOLDER + '/' +
                            image
                    ):
                        os.remove(
                            settings.MEDIA_ROOT + '/' +
                            settings.IMAGE_UPLOAD_FOLDER + '/' +
                            image
                        )

        return second_wrapper
    return first_wrapper
