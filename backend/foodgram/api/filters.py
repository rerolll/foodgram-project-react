from django_filters import rest_framework as filter
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter


class IngredientFilter(SearchFilter):
    search_param = "name"


class RecipeFilter(filter.FilterSet):
    author = filter.CharFilter()
    tags = filter.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        label="Tags",
        to_field_name="slug",
    )
    is_favorited = filter.BooleanFilter(field_name="is_favorited")
    is_in_shopping_cart = filter.BooleanFilter(
        field_name="is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = ["tags", "author", "is_favorited", "is_in_shopping_cart"]
