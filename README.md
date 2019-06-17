# aggregator_platform

* Django rest api - Authentication
* Channels - real time notifications(web sockets)

This project has two user roles - 
* Store manager and 
* Delivery person.

Task states, 
   1. New - initially when its created/not accepted by any delivery person
   2. Accepted - Once the delivery persons accepts
   3. Completed/Declined - these actions can be taken by delivery person once he/she accepts it
   4. Canceled - A manager(who created the task) can cancel only if its not accepted by any person
   
Task priorities, 
   1. Low,
   2. Medium,
   3. High

List of endpoints,

=> /manager/list_tasks - self explanatory

=> /manager/create_task - A manager can create a task with certain priority level.

=> /manager/cancel_task - To cancel a task which is not accepted by any delivery persons

=> /manager/list_transactions - Will list all the details/transactions of that particular task


=> /delivery_person/list_tasks  - (self explanatory)

=> /delivery_person/accept_task

=> /delivery_person/complete_task

=> /delivery_person/decline_task


All these actions taken by the delivery person will be notified the manager and any higher priority task created by manager will be updated to all delivery persons in a real-time websockets(channels).
