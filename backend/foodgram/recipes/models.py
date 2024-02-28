from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


MIN_VALUE_INGREDIENTS = 1
MIN_COOKING_TIME = 1
MAX_LENGTH_NAME = 200
MAX_COLOR_LENGTH = 7
MAX_SLUG_LENGTH = 200


class Ingredient(models.Model):
    name = models.CharField("Название ингредиента", max_length=MAX_LENGTH_NAME)
    measurement_unit = models.CharField(
        "Единицы измерения", max_length=MAX_SLUG_LENGTH
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="ingredient_name_unit_unique",
            )
        ]


class Tag(models.Model):
    name = models.CharField(
        "Название тега", unique=True, max_length=MAX_LENGTH_NAME
    )
    color = models.CharField("Цвет", unique=True, max_length=MAX_COLOR_LENGTH)
    slug = models.SlugField("Slug", unique=True, max_length=MAX_SLUG_LENGTH)

    class Meta:
        ordering = ["name"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag, through="RecipeTag", verbose_name="Теги", related_name="tags"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", verbose_name="Ингредиенты"
    )
    image = models.ImageField("Изображение", upload_to="recipes/images/")
    name = models.CharField("Название рецепта", max_length=MAX_LENGTH_NAME)
    text = models.TextField(
        "Описание рецепта", help_text="Введите описание рецепта"
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления",
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                message="Время приготовления должно быть не менее 1 минуты!",
            )
        ],
    )
    pub_date = models.DateTimeField(
        "Время публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент"
    )
    amount = models.IntegerField(
        "Количество", validators=[MinValueValidator(MIN_VALUE_INGREDIENTS)]
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="recipe_ingredient_unique",
            )
        ]


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["recipe", "tag"], name="recipe_tag_unique"
            )
        ]


class FavoriteShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )

    class Meta:
        abstract = True
        constraints = [
            UniqueConstraint(
                fields=("user", "recipe"),
                name="%(app_label)s_%(class)s_unique",
            )
        ]


class ShoppingCart(FavoriteShoppingCart):
    class Meta:
        default_related_name = "shopping_cart"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Favorite(FavoriteShoppingCart):
    class Meta:
        default_related_name = "favorites"
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
