from dataclasses import asdict
from app.infra.db.sql_mapper import SQLMapper
from app.infra.db.models.recipe.recipe_model import RecipeModel
from app.infra.db.refactor.mysql_executor import MySQLExecutor


class RecipeDao:
    def __init__(self):
        self.__mapper = SQLMapper('Recipe', RecipeModel)

    def find(self, executor: MySQLExecutor, recipe_id: int) -> RecipeModel:
        query = 'SELECT * FROM Recipe WHERE id = %s'
        data = (recipe_id,)
        result = executor.find(query, data)

        return self.__mapper.from_tuple(result) if result else None

    def findAll(self, executor: MySQLExecutor, name: str = None):
        query = "SELECT * FROM Recipe"
        data = {}

        if name is not None:
            query += " WHERE LOWER(name) LIKE LOWER(%(name)s)"
            data['name'] = f'%{name}%'

        results = executor.findAll(query, data)

        return self.__mapper.from_tuples(results)

    def save(self, executor: MySQLExecutor, recipe_model: RecipeModel) -> int:
        query = f'INSERT INTO {recipe_model.table_name()} {recipe_model.insert_columns_template()} VALUES {recipe_model.insert_values_template()}'
        data = asdict(recipe_model)

        return executor.create(query, data)