About:

-> A web-based Hospital Management System developed using Flask with server-side rendering.  
-> This project focuses on managing hospital-related workflows with manual authentication logic and database-driven operations.

Overview:  
-> This Hospital Management System is built using Flask as the backend framework and follows a traditional server-rendered web application approach.  
-> Instead of using frontend frameworks or REST APIs, the application renders HTML pages directly using Flask templates.  
-> The system demonstrates core backend concepts such as routing, database modeling, authentication, authorization, and data visualization.  

Tech Stack:  
Backend:  
-> Flask – Web framework for routing and backend logic  
-> SQLAlchemy – ORM for database modeling and operations  
-> Werkzeug – Used for password hashing and verification  
Frontend:  
-> HTML – Template structure  
-> Bootstrap (CDN) – Styling and responsive UI  
-> CSS & JavaScript – Client-side enhancements  

Database:  
-> SQLite (via SQLAlchemy models[ORM based])  

Application Architecture:  
-> Server-side Rendering  
-> Pages are rendered using Flask’s render_template() function.  
-> No JSON-based API communication  
-> Data is passed directly from Flask routes to templates and accessed using Jinja2 templating instead of JSON responses.  

Template Engine:  
-> Jinja2 is used to dynamically display data  
-> Variables, loops, and conditionals are handled within HTML templates  

Authentication & Authorization:  
-> Authentication and authorization are implemented manually  
-> No external security frameworks or authentication libraries are used  
-> Password hashing and unhashing is done using werkzeug.security  
-> Role-based or permission logic is handled within application logic  

Data Visualization:  
-> Charts are generated to visualize hospital-related data  
-> Useful for insights such as patient statistics or activity summaries  
-> Implemented using frontend JavaScript charting logic
