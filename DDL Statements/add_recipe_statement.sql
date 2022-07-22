## For adding recipe data into food.recipe database

INSERT INTO food.recipes (created_ts, name, type, difficulty_status, url)
VALUES(CURRENT_TIMESTAMP, 'Cheesecake', 'Dessert', 'Medium', 'https://sugarspunrun.com/best-cheesecake-recipe/');
