# Django Models Cheatsheet

- Define our model in models file
- Register the app in settings file
- You can makemigrations and migrate now
- You can create custom model fields
- If you are not providing a column to serve as the primary key, then django will automatically add one for you. But if you expliciity set a column to be a primary key, then django won't add a new column to be the primary key.
- Every field has verbose name (first positional argument, excluding ForignKey, ManyToManyField, OneToOneField)
- Many to one relationship use ForeignKey
- To define many to many relationship you hae to use ManyToManyField in one of two models you defined. It's not important which one have the field, but you have to make sure that only one model has the field.
- You can also define an intermediary model to connect two models which have many to many relationship, by providing through argument in ManyToManyField.
- 