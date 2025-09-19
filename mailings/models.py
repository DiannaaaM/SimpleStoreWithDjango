from django.db import models
from django.conf import settings


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Ф. И. О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients',
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        permissions = (
            ("can_view_all_clients", "Менеджер: может просматривать всех клиентов"),
        )

    def __str__(self):
        return f"{self.full_name} <{self.email}>"


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages',
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = (
            ("can_view_all_messages", "Менеджер: может просматривать все сообщения"),
        )

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CREATED = 'created'
    STATUS_RUNNING = 'running'
    STATUS_FINISHED = 'finished'
    STATUS_CHOICES = (
        (STATUS_FINISHED, 'Завершена'),
        (STATUS_CREATED, 'Создана'),
        (STATUS_RUNNING, 'Запущена'),
    )

    start_at = models.DateTimeField(verbose_name='Дата и время первой отправки')
    finish_at = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings', verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, related_name='mailings', verbose_name='Получатели')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mailings',
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = (
            ("can_view_all_mailings", "Менеджер: может просматривать все рассылки"),
            ("can_disable_mailings", "Менеджер: может отключать рассылки"),
        )

    def __str__(self):
        return f"Рассылка #{self.pk} — {self.get_status_display()}"


class MailingAttempt(models.Model):
    STATUS_SUCCESS = 'success'
    STATUS_FAIL = 'fail'
    STATUS_CHOICES = (
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAIL, 'Не успешно'),
    )

    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(blank=True, verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts', verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='attempts', verbose_name='Получатель')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return f"{self.get_status_display()} at {self.attempted_at}"


