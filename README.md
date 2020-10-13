# elementor
de test


I've had a bit of time issue, tried to go the API route but it was taking too much time and resorted to one file answer (main.py)

i've used postgtres as the db 

the current solution reads from the file, and create a website table for each site as well as a tracking table so we know when the site was last tracked.
it only updates table if last_tracked most recent timestamp is more the 30 mn away. 
Ive used update columns or insert id this is first time checking the site, though i should have just done inserts with timestamp of the update ...


i used the API fro vT site, and used a public API in my soultion, having chosen this route i was not able to fetch the category data as requested in 1.iii.
Another way may be was to use pandas.to_html function that should yeld the same data table.


AWS implement:
in real world I will read the data from the API fetching it on a timely basis (say 30 minutes) and insert it to relvant bucket on S3.

I would use a workflow tool like Airflow to process ETL data from S3 to redshift and update given tables if there is data to update.

i will same logic for if to update: create a tracking table and if and only if last track was done moer than 30 min i would update buckets.







