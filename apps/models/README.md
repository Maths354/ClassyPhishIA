# Models.py

Contains database tables, this is where new tables have to be declared

---
# Post.py

This file is used to insert things into tables

## Functions

The function `insert_table()` is used to insert values in every tables

Parameter : 

`upload` : this variable take into value a table with data

Example : 

First of all, you have to define your variable for example we will name it here official_site

```
official_site = OfficalSite(url="www.orange.fr", list_url="list_url", logo="logo", key_word="key_word", certificate="certificate", template="template")
```

As we can see, the variable take as a value a Class named OfficialSite, this will refer to the Class available into `Models.py` file

So there's 4 classes that can be called : 
- OfficialSite
- PhishingSite
- Score
- ReccurentDomain

In the parameter of the class that you call, you have to define the values that you want to add into the table.

In the next step, you have to call the function `insert_table()`

```
Post().insert_table(upload=official_site)
```




The function `update_recurrant_domain()` is used to insert domain values in ReccurentDomain table

Parameter : 

`phishing_link` : this variable take into value a link

Example : 

You only have to call the function like this and put in parameter your phishing link.

```
Post().update_recurrant_domain(phishing_link=phishing_link)
```



---
# Questions.py

This file is used to get things from tables

## Functions

The function `get_all_table()` it's like a `SELECT * FROM my_table;`

Parameter : 

`table` : this variable take into value the name of a table class 

Example : 

To call the function you have to call it like that : 
```
my_datas=Questions().get_all_table(OfficialSite)
my_datas=Questions().get_all_table(PhishingSite)
my_datas=Questions().get_all_table(Score)
my_datas=Questions().get_all_table(ReccurentDomain)
```

Your variable will get a dictionnary with values from the table selected.




The function `get_table_with_id()` it's like a `SELECT * FROM my_table WHERE id=my_id;`

Parameter : 

`table` : this variable take into value the name of a table class 
`id` : the id means the primary key of the table selected in the variable `table`

Example : 

To call the function you have to call it like that : 

```
my_datas=Questions().get_table_with_id(OfficalSite,1)
my_datas=Questions().get_table_with_id(ReccurentDomain,"com")
my_datas=Questions().get_table_with_id(PhishingSite,3)
my_datas=Questions().get_table_with_id(Score,5)
```