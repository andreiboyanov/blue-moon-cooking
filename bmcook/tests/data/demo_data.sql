insert into recipes(name, description, preparation)
values ('Meat balls',
        'Pork meat balls',
        'Combine the milk and breadcrumbs. Whisk the egg, salt, pepper, Parmesan, and parsley. Add the ground meat. Add the onions and soaked breadcrumbs.
        Form the meat into meatballs.
        Option 1: Roast or broil the meatballs in the oven.
        Option 2: Cook the meatballs directly in sauce.');


insert into recipes(name, description, preparation)
values ('Onion soup',
        'French onion soup',
        'Peel and crush the garlic, peel and slice the onions and shallots. Trim, wash and slice the leeks.
        Put the butter, 2 lugs of olive oil, the sage leaves (reserving 8 for later) and the crushed garlic into a
        thick-bottomed, non-stick pan. Stir everything round and add the onions, shallots and leeks. Season with
        sea salt and black pepper.
        Place a lid on the pan, leaving it slightly ajar, and cook slowly for 50 minutes, without colouring the
        vegetables too much. Remove the lid for the last 20 minutes – your onions will become soft and golden.
        Stir occasionally so that nothing catches on the bottom. Having the patience to cook the onions slowly,
        slowly, gives you an incredible sweetness and an awesome flavour, so don’t be tempted to speed this bit up.
        When your onions and leeks are lovely and silky, add the stock. Bring to the boil, turn the heat down and
        simmer for 10 to 15 minutes. You can skim any fat off the surface if you like, but I prefer to leave it
        because it adds good flavour.
        Preheat the oven or grill to maximum.
        Toast your bread on both sides. Correct the seasoning of the soup. When it’s perfect, ladle it into
        individual heatproof serving bowls and place them on a baking tray.
        Tear toasted bread over each bowl to fit it like a lid. Feel free to push and dunk the bread into the
        soup a bit. Grate over some of the Cheddar and drizzle over a little Worcestershire sauce.
        Dress your reserved sage leaves with some olive oil and place one on top of each slice of bread.
        Put the baking tray into the preheated oven or under the grill to melt the cheese until bubbling and golden.
        Keep an eye on it and make sure it doesn’t burn! When the cheese is bubbling, very carefully lift out the tray
        and carry it to the table. Enjoy');

insert into tags(tag)
values ('meet');
insert into tags(tag)
values ('pork');
insert into tags(tag)
values ('french soup');
insert into tags(tag)
values ('onion');

insert into ingredients(name)
values ('meet');
insert into ingredients(name)
values ('onion');
insert into ingredients(name)
values ('peper');
insert into ingredients(name)
values ('salt');
insert into ingredients(name)
values ('breadcrumbs');
insert into ingredients(name)
values ('egg');
insert into ingredients(name)
values ('garlic');
insert into ingredients(name)
values ('red onion');
insert into ingredients(name)
values ('white onions');
insert into ingredients(name)
values ('banana shallots');
insert into ingredients(name)
values ('leeks');
insert into ingredients(name)
values ('butter');
insert into ingredients(name)
values ('olive oil');
insert into ingredients(name)
values ('fresh sage leaves');
insert into ingredients(name)
values ('organic beef, vegetable or chicken stock');
insert into ingredients(name)
values ('good-quality stale bread');
insert into ingredients(name)
values ('Cheddar cheese');
insert into ingredients(name)
values ('Worcestershire sauce');

insert into recipe_ingredients
values (1, 1, 500, 'g');
insert into recipe_ingredients
values (1, 2, 1, 'pcs');
insert into recipe_ingredients
values (1, 3, null, null);
insert into recipe_ingredients
values (1, 4, null, null);
insert into recipe_ingredients
values (1, 5, 2, 'teaspoons');
insert into recipe_ingredients
values (1, 6, 1, 'pcs');

insert into recipe_ingredients
values (2, 7, 6, 'cloves');
insert into recipe_ingredients
values (2, 8, 5, 'pcs');
insert into recipe_ingredients
values (2, 9, 3, 'pcs');
insert into recipe_ingredients
values (2, 10, 3, 'pcs');
insert into recipe_ingredients
values (2, 11, 300, 'g');
insert into recipe_ingredients
values (2, 12, 100, 'g');
insert into recipe_ingredients
values (2, 13, null, null);
insert into recipe_ingredients
values (2, 14, 1, 'good handful');
insert into recipe_ingredients
values (2, 15, 2, 'liters');
insert into recipe_ingredients
values (2, 16, 8, 'cm');
insert into recipe_ingredients
values (2, 17, 200, 'g');
insert into recipe_ingredients
values (2, 18, null, null);

insert into recipe_tags
values (1, 1);
insert into recipe_tags
values (1, 2);
insert into recipe_tags
values (2, 3);
insert into recipe_tags
values (2, 4);
