create table students (
student_id      int generated always as identity primary key,
full_name       text not null, 
email           text unique not null,
birth_date      date, 
enrollment_date date not null default current_date
);

create table courses (
course_id       int generated always as identity primary key, 
course_name     text not null,
instructor_name text not null,
credits         int check (credits > 0) not null
);

create table grades (
grade_id        int generated always as identity primary key, 
student_id      int not null references students(student_id),
course_id       int not null references courses(course_id),
grade           numeric(5, 2) not null check (grade >= 0 and grade <= 100),
unique          (student_id, course_id) 
);

insert into courses (course_name, instructor_name, credits)
values ('postgresql', 'Vladimir egay', 3),
       ('python', 'Vladimir egay', 3),
       ('AI', 'Vladimir egay', 3);


insert into students (full_name, email)
values ('Jhung min', 'someone@gmail.com'),
       ('JJ', 'JJ@gmail.com'),
       ('Nikita', 'nikita@gmail.com');


insert into grades (student_id, course_id, grade)
values (1, 1, 75.3),
       (2, 2, 99.98),
       (3, 2, 99.98),
       (1, 3, 75.99);
       
update students 
set full_name = 'Elon musk'
where email = 'someone@gmail.com'; 

update students 
set full_name = 'Tony Stark'
where email = 'JJ@gmail.com';

delete from grades
where student_id = 1;

delete from students 
where student_id = 1; 









