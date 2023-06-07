drop table if exists tags cascade;
create table tags
(
    id  serial not null
        constraint tag_pk
            primary key,
    tag varchar(50)    not null
        constraint tags_pk
            unique
);
alter table tags owner to moon;

drop table if exists ingredients cascade;
create table ingredients
(
    id  serial not null
        constraint ingredients_pk
            primary key,
    name        varchar(50)
        constraint ingredients_pk2
            unique,
    description integer
);
alter table ingredients owner to moon;

drop table if exists recipes cascade ;
create table recipes
(
    id  serial not null
        constraint recipe_pk
            primary key,
    name        varchar(50)
        constraint recipe_pk2
            unique,
    description varchar,
    cooking_time int,
    preparation varchar
);
alter table recipes owner to moon;

drop table if exists recipe_ingredients;
create table recipe_ingredients
(
    recipe_id     integer not null
        constraint recipe_ingredients_recipe_id_fk
            references recipes
            on delete cascade,
    ingredient_id integer not null
        constraint recipe_ingredients_ingredients_id_fk
            references ingredients
            on delete cascade,
    quantity      integer,
    unit          varchar(50),
    constraint recipe_ingredients_pk
        primary key (recipe_id, ingredient_id)
);
alter table recipe_ingredients owner to moon;

drop table if exists recipe_tags;
create table recipe_tags
(
    recipe_id integer not null
        constraint recipe_tags_recipes_id_fk
            references recipes,
    tag_id    integer not null
        constraint recipe_tags_tags_id_fk
            references tags,
    constraint recipe_tags_pk
        primary key (recipe_id, tag_id)
);
alter table recipe_tags owner to moon;

