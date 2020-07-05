# API
Where we can fetch our data from. Eventually, we want to reshape this so that it uses strategy models to calculate relevant data and expose it to our apps.

## Endpoints
+ `GET '/'`: returns success message
+ `GET '/current'`: return JSON object containing current data
>{<br>
>   "elevation": 2.33051380781163e+17, <br>
>   "entry_time": "2020-06-20T17:43:22.981400", <br>
>   "recommended_velocity": -39.8884, <br>
>   "velocity": 17.096 <br>
>}
+ `GET '/previous/<time_in_minutes>'`: returns JSON array containing data logged within `time_in_minutes` before current time. Each element of array will take same form as response from `/current`.