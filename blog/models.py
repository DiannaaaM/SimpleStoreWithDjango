from django.db import models


class Post(models.Model):
    name = models.CharField(max_length=100, verbose_name="Заголовок поста", help_text="Укажите заголовок поста")
    description = models.TextField(verbose_name="Основной текст", help_text="Введите текст поста", blank=True,
                                   null=True)
    image = models.ImageField(upload_to="post/image", blank=True, null=True, verbose_name="Обложка",
                              help_text="Добавьте изображение для поста")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added", help_text="Date Added", blank=True,
                                      null=True)
    was_publication = models.BooleanField(default=True, verbose_name="Опубликовано", help_text="Статус публикации поста")
    views_counter = models.PositiveIntegerField(verbose_name="Количество просмотров", help_text="Укажите количество просмотров", default=0)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["description", "name"]

    def __str__(self):
        return self.name
