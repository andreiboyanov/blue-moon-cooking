import psycopg2
import psycopg2.extras
from typing import TypedDict, Dict, List
from . import config
from bmcook.exceptions import RecipeDataError, RecipeIntegrityError

UPDATABLE_FIELDS = ["name", "description", "cooking_time", "preparation"]
M2M_FIELDS = ["ingredients", "tags"]


class IngredientType(TypedDict):
    id: int
    name: str
    quantity: int
    unit: str


class RecipeType(TypedDict):
    id: int
    name: str
    description: str
    cooking_time: int
    preparation: str
    tags: List[str]
    ingredients: List[IngredientType]


class RecipeDB:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.connection = psycopg2.connect(
            database=config.db_name,
            user=config.db_user,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port
        )
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    def close(self):
        self.cursor.close()
        self.connection.close()

    def _add_m2m_to_recipes(self, recipes: List[RecipeType]) -> None:
        ingredients_sql = """
            select * from recipe_ingredients ri
            inner join ingredients i
                on ri.ingredient_id = i.id
            where recipe_id = %s
        """
        tags_sql = """
            select * from recipe_tags rt
            inner join tags t
                on rt.tag_id = t.id
            where recipe_id = %s
        """
        for recipe in recipes:
            self.cursor.execute(
                ingredients_sql, (recipe["id"],)
            )
            recipe["ingredients"] = self.cursor.fetchall()
            self.cursor.execute(
                tags_sql, (recipe["id"],)
            )
            recipe["tags"] = [
                tag["tag"] for tag in self.cursor.fetchall()
            ]

    def _update_m2m(self, recipe_id: int, recipe: RecipeType) -> None:
        if "ingredients" in recipe:
            self.add_ingredients(recipe_id, recipe["ingredients"])
        if "tags" in recipe:
            self.add_tags(recipe_id, recipe["tags"])

    def get_recipes(self, skip: int = 0, limit: int = 10) -> (
            List[RecipeType] or None
    ):
        sql = """
            select * from recipes
            order by id
            limit %s offset %s
        """
        self.cursor.execute(sql, (limit, skip))
        rows = self.cursor.fetchall()
        self._add_m2m_to_recipes(rows)
        return rows or None

    def get_recipe(self, recipe_id: int) -> RecipeType or None:
        sql = """
            select * from recipes
            where id = %s
        """
        self.cursor.execute(sql, (recipe_id,))
        rows = self.cursor.fetchall()
        self._add_m2m_to_recipes(rows)
        return rows[0] if len(rows) > 0 else None

    def search_recipes_by_keywords(self, query: str, skip: int = 0,
                                   limit: int = 10) -> List[RecipeType] or None:
        sql = """
            with 
            
            ingredient_vectors as (select recipe_id, string_agg(name, ' ') 
            ingredient_names from ingredients
            inner join recipe_ingredients ri
                on ingredients.id = ri.ingredient_id
            group by recipe_id),
            
            tag_vectors as (select recipe_id, string_agg(tag, ' ') 
            tag_names from tags
            inner join recipe_tags rt
                on tags.id = rt.tag_id
            group by recipe_id)
            
            select r.* from recipes r
                     inner join ingredient_vectors i
                        on r.id = i.recipe_id
                     inner join tag_vectors t
                        on r.id = t.recipe_id
            where to_tsvector(
                preparation
                    || ' '
                    || description
                    || ' '
                    || ingredient_names
                    || ' '
                    || tag_names
                ) @@ to_tsquery(%s)
            offset %s
            limit %s
            ;
        """
        ts_query = query.replace(" ", "|")
        self.cursor.execute(sql, (ts_query, skip, limit))
        rows = self.cursor.fetchall()
        self._add_m2m_to_recipes(rows)
        return rows or None

    def search_recipes_by_products(self, products: str, skip: int = 0,
                                   limit: int = 10) -> List[RecipeType] or None:
        sql = """
            with 

            ingredient_vectors as (select recipe_id, string_agg(name, ' ') 
            ingredient_names from ingredients
            inner join recipe_ingredients ri
                on ingredients.id = ri.ingredient_id
            group by recipe_id)

            select r.* from recipes r
                     inner join ingredient_vectors i
                        on r.id = i.recipe_id
            where to_tsvector(ingredient_names) @@ to_tsquery(%s)
            offset %s
            limit %s
            ;
        """
        ts_query = products.replace(" ", "|")
        self.cursor.execute(sql, (ts_query, skip, limit))
        rows = self.cursor.fetchall()
        self._add_m2m_to_recipes(rows)
        return rows or None

    def search_recipes_by_tags(self, tags: str, skip: int = 0,
                                   limit: int = 10) -> List[RecipeType] or None:
        sql = """
            with 

            tag_vectors as (select recipe_id, string_agg(tag, ' ') 
            tag_names from tags
            inner join recipe_tags rt
                on tags.id = rt.tag_id
            group by recipe_id)

            select r.* from recipes r
                     inner join tag_vectors t
                        on r.id = t.recipe_id
            where to_tsvector(tag_names) @@ to_tsquery(%s)
            offset %s
            limit %s
            ;
        """
        ts_query = tags.replace(" ", "|")
        self.cursor.execute(sql, (ts_query, skip, limit))
        rows = self.cursor.fetchall()
        self._add_m2m_to_recipes(rows)
        return rows or None

    def add_recipe(self, recipe: RecipeType,
                   recipe_id: int or None = None) -> None:
        if recipe_id is None:
            sql = """
                insert into recipes (
                    name, description, cooking_time, preparation
                ) values (
                    %(name)s, %(description)s, 
                    %(cooking_time)s, %(preparation)s
                )
                returning id
            """
        else:
            sql = """
                insert into recipes (
                id, name, description, cooking_time, preparation
                ) values (
                    %(id)s, %(name)s, %(description)s, 
                    %(cooking_time)s, %(preparation)s
                )
            """

        try:
            recipe.update(id=recipe_id)
            self.cursor.execute(sql, recipe)
            if recipe_id is None:
                result = self.cursor.fetchall()
                recipe_id = result[0]["id"]
            self._update_m2m(recipe_id, recipe)
            self.connection.commit()
        except psycopg2.IntegrityError as error:
            raise RecipeIntegrityError(error)
        except psycopg2.Error as error:
            raise RecipeDataError(error)

    def update_recipe(self, recipe_id: int, updates: RecipeType) -> None:
        """Updates a recipe with recipe_id
        Parameters
        ----------
        recipe_id: Recipe ID to update
        updates: dict with key:value pairs to update
        """
        sql = """
        update recipes set """
        sql += ",".join(
            [field + " = %s" for field in updates if field in UPDATABLE_FIELDS])
        sql += """
        where id = %s
        """
        try:
            self.cursor.execute(
                sql,
                [updates.get(field) for field in updates if
                 field in UPDATABLE_FIELDS] +
                [recipe_id]
            )
            self._update_m2m(recipe_id, updates)
            self.connection.commit()
        except psycopg2.Error as error:
            raise RecipeDataError(error)

    def replace_recipe(self, recipe_id: int, new_recipe: RecipeType) -> None:
        """Delete existing and create a new recipe
        Parameters
        ----------
        recipe_id: Recipe ID to update.
            If a recipe with the given ID exists it will be deleted.
        new_recipe: dict with the new recipe data.
            A recipe with this attributes will be created.
        """
        try:
            self.delete_recipe(recipe_id)
            self.add_recipe(new_recipe, recipe_id=recipe_id)
        except psycopg2.Error as error:
            raise RecipeDataError(error)

    def delete_recipe(self, recipe_id: int) -> None:
        sql = """
        delete from recipe_ingredients where recipe_id = %s;
        delete from recipe_tags where recipe_id = %s;
        delete from recipes where id = %s;
        """
        self.cursor.execute(sql, (recipe_id, recipe_id, recipe_id,))
        self.connection.commit()

    def add_ingredients(
            self, recipe_id: int, ingredients: List[IngredientType]
    ):
        sql = """
            delete from recipe_ingredients where recipe_id = %s
        """
        self.cursor.execute(sql, (recipe_id, ))
        for ingredient in ingredients:
            ingredient_id = self.get_or_create_ingredient(ingredient)
            self.add_ingredient_to_recipe(
                recipe_id, ingredient_id,
                ingredient["quantity"], ingredient["unit"]
            )

    def add_tags(
            self, recipe_id: int, tags: List[str]
    ):
        sql = """
            delete from recipe_tags where recipe_id = %s
        """
        self.cursor.execute(sql, (recipe_id, ))
        for tag in tags:
            tag_id = self.get_or_create_tag(tag)
            self.add_tag_to_recipe(recipe_id, tag_id)

    def get_or_create_ingredient(
            self,
            ingredient: IngredientType
    ) -> int:
        sql = """
            select * from ingredients
            where name = %s
        """
        self.cursor.execute(sql, (ingredient["name"], ))
        result = self.cursor.fetchall()
        if len(result) == 0:
            ingredient_id = self.add_ingredient(ingredient)
        else:
            ingredient_id = result[0]["id"]
        return ingredient_id

    def add_ingredient(self, ingredient: Dict[str, str]) -> int:
        sql = """
            insert into ingredients (name, description)
            values (%s, %s)
            returning id
        """
        self.cursor.execute(
            sql, (ingredient.get("name"), ingredient.get("description", ""))
        )
        result = self.cursor.fetchall()
        return result[0]["id"]

    def add_ingredient_to_recipe(
            self, recipe_id: int, ingredient_id: int,
            quantity: int, unit: str
    ) -> None:
        sql = """
            insert into recipe_ingredients values (%s, %s, %s, %s)
        """
        self.cursor.execute(
            sql,
            (recipe_id, ingredient_id, quantity, unit)
        )

    def get_or_create_tag(self, tag: str) -> int:
        sql = """
            select * from tags
            where tag = %s
        """
        self.cursor.execute(sql, (tag, ))
        result = self.cursor.fetchall()
        if len(result) == 0:
            tag_id = self.add_tag(tag)
        else:
            tag_id = result[0]["id"]
        return tag_id

    def add_tag(self, tag: str) -> int:
        sql = """
            insert into tags (tag)
            values (%s)
            returning id
        """
        self.cursor.execute(sql, (tag, ))
        result = self.cursor.fetchall()
        return result[0]["id"]

    def add_tag_to_recipe(self, recipe_id: int, tag_id: int,) -> None:
        sql = """
            insert into recipe_tags values (%s, %s)
        """
        self.cursor.execute(
            sql,
            (recipe_id, tag_id)
        )
