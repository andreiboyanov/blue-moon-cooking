insert into recipes(id, name, description, preparation) values (
    1,
    'Meat balls',
    'Pork meat balls',
    'Combine the milk and breadcrumbs. Whisk the egg, salt, pepper, Parmesan, and parsley. Add the ground meat. Add the onions and soaked breadcrumbs.
    Form the meat into meatballs.
    Option 1: Roast or broil the meatballs in the oven.
    Option 2: Cook the meatballs directly in sauce.'
);

insert into recipes(id, name, description, preparation) values (2,
                                                                'Onion soup',
                                                                'French onion soup',
                                                                '
    Peel and crush the garlic, peel and slice the onions and shallots. Trim, wash and slice the leeks.
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

insert into tags values(1, 'meet');
insert into tags values(2, 'pork');
insert into tags values(3, 'french soup');
insert into tags values(4, 'onion');

insert into ingredients values(1, 'meet');
insert into ingredients values(2, 'onion');
insert into ingredients values(3, 'peper');
insert into ingredients values(4, 'salt');
insert into ingredients values(5, 'breadcrumbs');
insert into ingredients values(6, 'egg');
insert into ingredients values(7, 'garlic');
insert into ingredients values(8, 'red onion');
insert into ingredients values(9, 'white onions');
insert into ingredients values(10, 'banana shallots');
insert into ingredients values(11, 'leeks');
insert into ingredients values(12, 'butter');
insert into ingredients values(13, 'olive oil');
insert into ingredients values(14, 'fresh sage leaves');
insert into ingredients values(15, 'organic beef, vegetable or chicken stock');
insert into ingredients values(16, 'good-quality stale bread');
insert into ingredients values(17, 'Cheddar cheese');
insert into ingredients values(18, 'Worcestershire sauce');

insert into recipe_ingredients values(1, 1, 500, 'g');
insert into recipe_ingredients values(1, 2, 1, 'pcs');
insert into recipe_ingredients values(1, 3, null, null);
insert into recipe_ingredients values(1, 4, null, null);
insert into recipe_ingredients values(1, 5, 2, 'teaspoons');
insert into recipe_ingredients values(1, 6, 1, 'pcs');

insert into recipe_ingredients values (2, 7, 6, 'cloves');
insert into recipe_ingredients values (2, 8, 5, 'pcs');
insert into recipe_ingredients values (2, 9, 3, 'pcs');
insert into recipe_ingredients values (2, 10, 3, 'pcs');
insert into recipe_ingredients values (2, 11, 300, 'g');
insert into recipe_ingredients values (2, 12, 100, 'g');
insert into recipe_ingredients values (2, 13, null, null);
insert into recipe_ingredients values (2, 14, 1, 'good handful'); 
insert into recipe_ingredients values (2, 15, 2, 'liters');
insert into recipe_ingredients values (2, 16, 8, 'cm'); 
insert into recipe_ingredients values (2, 17, 200, 'g');
insert into recipe_ingredients values (2, 18, null, null);


    select 2, id from ingredients where id > 6
;
insert into recipe_tags values(1, 1);
insert into recipe_tags values(1, 2);
insert into recipe_tags values(2, 3);
insert into recipe_tags values(2, 4);
