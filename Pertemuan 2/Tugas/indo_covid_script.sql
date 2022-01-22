SELECT jabar_csv.`date`, cases_csv.acc_confirmed, cases_csv.acc_negative, 
jabar_csv.positive_total, jabar_csv.odp_total 
FROM jabar_csv 
LEFT JOIN cases_csv 
ON jabar_csv.`date` = cases_csv.`date` 
WHERE cases_csv.acc_confirmed IS NOT NULL 
ORDER BY cases_csv.acc_negative DESC;

select * from cases_csv;
acc_confirmed 
acc_negative

select * from jabar_csv;
positive_total 
odp_total 

select ja.date, ca.acc_confirmed, ca.acc_negative, ja.positive_total, ja.odp_total 
from cases_csv ca
inner join jabar_csv ja
on ja.date = ca.date