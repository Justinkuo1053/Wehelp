
Task 2
● Create a new database named website.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/433afb7a-12ed-4fc5-9ebb-040b9b4f59d8)

● Create a new table named member, in the website database, designed as below:
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/d1fa6b90-7967-43fc-8948-907ee93886e7)

Task 3
● INSERT a new row to the member table where name, username and password must
be set to test. INSERT additional 4 rows with arbitrary data.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/a4114b56-426f-48b3-b5fc-a64cb47cca00)

● SELECT all rows from the member table.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/eb8b6841-2559-4b7c-8712-8742da0dd7c6)

● SELECT all rows from the member table, in descending order of time.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/b539d3f6-62ff-49fe-af02-3a5bd311e3b5)

● SELECT total 3 rows, second to fourth, from the member table, in descending order
of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/fb318913-a81e-4a25-b8b6-6ed21ff0038f)


● SELECT rows where username equals to test.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/ddab54fd-30a9-4435-810d-952ff0ddde13)

● SELECT rows where name includes the es keyword.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/460210b0-cc82-44e7-82cd-be87008f63bc)

● SELECT rows where both username and password equal to test.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/1425c9f6-fa3b-4a26-aeb7-d79d7b56f1c1)

● UPDATE data in name column to test2 where username equals to test.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/ee30a248-73a9-48da-9efe-4db737c94e09)

Task 4 
● SELECT how many rows from the member table.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/64a1dd99-d383-4530-b326-5799b5bb1dde)

● SELECT the sum of follower_count of all the rows from the member table.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/3d60b70b-8808-4111-bd8d-df6c6db347a1)

● SELECT the average of follower_count of all the rows from the member table.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/e8e842fe-b148-476e-a7d7-bd67e6a65f87)

● SELECT the average of follower_count of the first 2 rows, in descending order of
follower_count, from the member table.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/ac0a9156-24a0-429d-8f9d-0925d2e1c0ef)

Task 5: SQL JOIN
● Create a new table named message, in the website database. designed as below:
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/a20df365-4082-457c-af8b-a242ebf86054)
自行創建數據
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/15d76152-deb6-41db-9104-6f3a88db706c)

● SELECT all messages, including sender names. We have to JOIN the member table
to get that.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/27f5992f-40c5-442e-b432-b393482377da)

● SELECT all messages, including sender names, where sender username equals to
test. We have to JOIN the member table to filter and get that.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/79954163-b770-41e6-8bf6-118f351e6379)
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/dc31511f-6aa6-4621-8104-2ea056bdb51d)


● Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like
count of messages where sender username equals to test.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/0d388e8e-f6f4-41ee-b65b-28be705a8d80)

● Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like
count of messages GROUP BY sender username.
![image](https://github.com/Justinkuo1053/wehelp/assets/57930354/498347cc-58ee-422e-a9e1-0b788aff290a)
