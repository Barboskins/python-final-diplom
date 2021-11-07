from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator
from django.db import models

"""Создаем модели и их дополнительные методы"""
STATUS_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),

)


class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('"Users must have an email address!"')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Стандартная модель пользователей
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    email = models.EmailField(verbose_name=_('email address'), unique=True)
    company = models.CharField(verbose_name=_('Компания'), max_length=40, blank=True)
    position = models.CharField(verbose_name=_('Должность'), max_length=40, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=40,
        blank=True,
        null=True,
        help_text=_('Name and last name. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    type = models.CharField(
        verbose_name=_('Тип пользователя'),
        choices=USER_TYPE_CHOICES,
        max_length=5,
        default='buyer'
    )

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _("Список пользователей")
        ordering = ('email',)

class Shop(models.Model):
    __tablename__ = 'Shop'
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    url = models.URLField(null=False, unique=True)
    filename = models.CharField(max_length=200, null=False, unique=True)


class Category(models.Model):
    __tablename__ = 'Category'
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories')
    name = models.CharField(max_length=100)

class Product(models.Model):
    __tablename__ = 'Product'
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class ProductInfo(models.Model):
    __tablename__ = 'ProductInfo'
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    price_rrc = models.PositiveIntegerField()

class Parameter(models.Model):
    __tablename__='Parameter'
    name = models.CharField(max_length=200)

class ProductParameter(models.Model):
    __tablename__ = "ProductParameter"
    product_info = models.ForeignKey(ProductInfo, blank=True, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, blank=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

class Order(models.Model):
    __tablename__ = "Order"
    user = models.ForeignKey(Parameter, blank=True, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    state = models.BooleanField()

class OrderItem(models.Model):
    __tablename__ = "OrderItem"
    order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Contact(models.Model):
    __tablename__ = "contact"
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

class ConfirmEmailToken(models.Model):
    """ Модель токена подтверждения электронной почты """

    class Meta:
        verbose_name = 'Токен подтверждения Email'
        verbose_name_plural = 'Токены подтверждения Email'

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        User,
        related_name='confirm_email_tokens',
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this password reset token")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("When was this token generated")
    )

    # Key field, though it is not the primary key of the model
    key = models.CharField(
        _("Token"),
        max_length=64,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)




