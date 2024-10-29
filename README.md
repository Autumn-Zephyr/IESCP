# Influencer Engagement and Sponsorship Coordination Platform 
## Modern Application Development - I, May 2024


> ### **My Details**

**Name:** Sneha Sarkar

**About Me:** I have always been passionate about coding since the time I was introduced to this programming world. I started my coding journey at the age of 13 with HTML. Later, at the age of 14 I was introduced to the programming language Java and hence tried to master myself in this language for 5 years. And therefore, I have a strong grip of Data Structures and Algorithms in this language.


> ### **Description** 

A platform for sponsors and influencers to interact with each other where a sponsor can launch campaigns and request advertisements to a particular influencer and an influencer can negotiate the amount offered by the sponsor and vice versa.


> ### **Technologies Used**

+ **Flask:** A lightweight Python web framework for building web applications.
+ **SQLite3:** A serverless, self-contained SQL database engine for storing application data.
+ **SQLAlchemy:** An ORM library for Python that provides a high-level interface for database operations.
+ **HTML:** The markup language for structuring web content.
+ **JavaScript (JS):** A scripting language for adding interactivity and dynamic behavior to web pages.
+ **JQuery:** A fast, lightweight JavaScript library that simplifies HTML document traversal, event handling, and animation.
+ **CSS:** A stylesheet language for controlling the appearance and layout of web pages.
+ **Datetime:** A Python module for handling and manipulating date and time information.
+ **Jinja2:** A templating engine for dynamically generating HTML content in Flask applications.
+ **Matplotlib:** A Python library for creating static, animated, and interactive visualizations.
+ **Flask-RESTful:** An extension for building REST APIs in Flask with ease.


> ### **DB Schema Design**

![ERD](/static/images/ERD.jpg)


> ### **API Design**

![ERD](/static/images/API.jpg)


> ### **Architecture** 

+ The **app.py** and **README.md** files, and the **templates**, **static**, **backend** and **instance** folders reside inside the **Codes** folder.
+ The **templates** folder contains all the **.html** files.
+ The **static** folder contains the **css**, **images** and **graphs** folders which further contains all **.css**, **.png** and all required graphs, respectively.
+ The **backend** folder contains other python files like **controllers.py**, **models.py**, **influencer.py**, **sponsor.py**, **admin.py** and **api.py**.


> ### **Features** 

+ The **Flag** and **Unflag** features allow the admins to flag inappropriate users or campaigns when found so and unflag them when the issue is resolved.
+ The **View** feature allows the users and admins to view campaigns, advertisements, and users based on their view permit.
+ The **Request** feature allows the influencers to send an ad request to the sponsors and vice versa.
+ The **Negotiate** feature allows the influencers/sponsors to negotiate the amount offered to/asked from them by the sponsors/influencers.
+ The **Task Completed** feature allows the influencers to inform the sponsors about the completion of the advertising task.
+ The **Pay & Mark as Complete** feature allows the sponsors to pay the influencers after work completion and officially declare the completion of advertising tasks.


