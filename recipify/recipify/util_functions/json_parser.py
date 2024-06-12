def parseRecipes(recipeJson):
    dish_names = []
    ingredients_list = []
    recipes_list = []

    for item in recipeJson['list']:
        dish_names.append(item['dish_name'])
        ingredients_list.append(item['ingredients_required'])
        recipes_list.append(item['recipe'])

    num_recipes = len(recipeJson['list'])

    return num_recipes, dish_names, ingredients_list, recipes_list


#DATA FOR TESTING
# data = {
#     'list': [
#         {
#             'dish_name': 'Kiwi Orange Smoothie',
#             'ingredients_required': [
#                 '3 Kiwis, peeled and chopped',
#                 '1 Orange, peeled and segmented',
#                 '1/2 cup Ice (optional)',
#                 '1/4 cup Water or Juice (optional)'
#             ],
#             'recipe': [
#                 '- Combine kiwis, orange segments, ice (if using), and water or juice (if using) in a blender.',
#                 '- Blend until smooth.',
#                 '- Pour into glasses and enjoy immediately.'
#             ]
#         }
#     ]
# }

# # Call the function and print the results
# num_recipes, dish_names, ingredients_list, recipes_list = parseRecipes(data)
# print(f"Number of Recipes: {num_recipes}")
# print(f"Dish Names: {dish_names}")
# print(f"Ingredients List: {ingredients_list}")
# print(f"Recipes List: {recipes_list}")
