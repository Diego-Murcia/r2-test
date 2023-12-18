# Instrucciones
1. Descargar los paquetes necesarios para correr el proyecto con los siguientes comandos:
    ```cmd
    pip install aiohttp asyncpg Flask 
    ```
   <br/>
2. Iniciar un contenedor de Docker con PostgreSQL utilizando el siguiente docker-compose.yaml:
   ```dockerfile
   version: '3.8'
   
   services:
     postgres:
       image: postgres:latest
       environment:
         POSTGRES_DB: r2_db
         POSTGRES_USER: r2_user
         POSTGRES_PASSWORD: secret
       ports:
         - "5432:5432"
   ```
   <br/>
3. Conectarse a la base de datos y ejecutar los siguientes scripts para la creación de las tablas necesarias para utilizar este proyecto:
   ```postgresql
   create table book(
    id varchar primary key,
    title varchar,
    subtitle varchar,
    publish_date varchar,
    editor varchar,
    description varchar,
    image varchar
   );
   
   create table author(
    id bigserial primary key,
    name varchar unique
   );
   
   create table category(
    id bigserial primary key,
    name varchar unique
   );
   
   create table book_author(
    book_id varchar references book(id),
    author_id bigint references author(id),
    primary key (book_id, author_id)
   );
   
   create table book_category(
    book_id varchar references book(id),
    category_id bigint references category(id),
    primary key (book_id, category_id)
   );
   ```
   <br/>
4. Correr el archivo *main.py* y utilizar la API en la carpeta llamada *postman* para probar su funcionalidad.