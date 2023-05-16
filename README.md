<h2> Import the data into Neo4j </h2>


CALL apoc.load.json('https://raw.githubusercontent.com/mneedham/bbcgoodfood/master/stream_all.json') YIELD value
WITH value.page.article.id AS id,
       value.page.title AS title,
       value.page.article.description AS description,
       value.page.recipe.cooking_time AS cookingTime,
       value.page.recipe.prep_time AS preparationTime,
       value.page.recipe.skill_level AS skillLevel
MERGE (r:Recipe {id: id})
SET r.cookingTime = cookingTime,
    r.preparationTime = preparationTime,
    r.name = title,
    r.description = description,
    r.skillLevel = skillLevel;

//import ingredients and connect to recipes
CALL apoc.load.json('https://raw.githubusercontent.com/mneedham/bbcgoodfood/master/stream_all.json') YIELD value
WITH value.page.article.id AS id,
       value.page.recipe.ingredients AS ingredients
MATCH (r:Recipe {id:id})
FOREACH (ingredient IN ingredients |
  MERGE (i:Ingredient {name: ingredient})
  MERGE (r)-[:CONTAINS_INGREDIENT]->(i)
);

//import collections and connect to recipes
CALL apoc.load.json('https://raw.githubusercontent.com/mneedham/bbcgoodfood/master/stream_all.json') YIELD value
WITH value.page.article.id AS id,
       value.page.recipe.collections AS collections
MATCH (r:Recipe {id:id})
FOREACH (collection IN collections |
  MERGE (c:Collection {name: collection})
  MERGE (r)-[:COLLECTION]->(c)
);



MATCH (:Collection {name: 'Snack'})<-[:COLLECTION]-(recipe)
RETURN recipe.id, recipe.name, recipe.description

MATCH (:Collection {name: 'Dinner party main'})<-[:COLLECTION]-(recipe)
RETURN  recipe.name, recipe.skillLevel, recipe.preparationTime

MATCH (:Collection {name: 'Muffin'})<-[:COLLECTION]-(recipe)
RETURN  recipe.name, recipe.skillLevel


:param allergens =>   [];
:param ingredients => ['cheese', 'flour'];


MATCH (r:Recipe)

WHERE all(i in $ingredients WHERE exists(
  (r)-[:CONTAINS_INGREDIENT]->(:Ingredient {name: i})))
AND none(i in $allergens WHERE exists(
  (r)-[:CONTAINS_INGREDIENT]->(:Ingredient {name: i})))

RETURN r.name AS recipe,
       [(r)-[:CONTAINS_INGREDIENT]->(i) | i.name]
       AS ingredients, r.skillLevel as Level
ORDER BY size(ingredients)
LIMIT 40

MATCH (r:Recipe)

WHERE r.skillLevel = "Easy"

RETURN r.name AS recipe,
       [(r)-[:CONTAINS_INGREDIENT]->(i) | i.name]
       AS ingredients, r.skillLevel as Level
