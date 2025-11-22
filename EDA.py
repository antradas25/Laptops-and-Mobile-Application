# use laptops;

# SELECT * FROM laptops;

# select * from laptops order by id limit 5

# SELECT * FROM laptops;

# -- head, tail and sample
# SELECT * FROM laptops
# ORDER BY `id` LIMIT 5;

# SELECT * FROM laptops
# ORDER BY `id` DESC LIMIT 5;

# SELECT * FROM laptops
# ORDER BY rand() LIMIT 5;

# select Price,
# MIN(Price) OVER(),
# MAX(Price) OVER(),
# AVG(Price) OVER(),
# STD(Price) OVER() 
# from laptops order by `id` limit 1;

# SELECT COUNT(Price)
# FROM laptops
# WHERE Price IS NULL

# SELECT COUNT(Price)
# FROM laptops
# WHERE Price IS NULL;

# SELECT 
#     t.buckets,
#     REPEAT('*', COUNT(*) / 5) AS histogram
# FROM (
#     SELECT Price,
#            CASE 
#                WHEN Price BETWEEN 0 AND 25000 THEN '0-25K'
#                WHEN Price BETWEEN 25001 AND 50000 THEN '25K-50K'
#                WHEN Price BETWEEN 50001 AND 75000 THEN '50K-75K'
#                WHEN Price BETWEEN 75001 AND 100000 THEN '75K-100K'
#                ELSE '>100K'
#            END AS buckets
#     FROM laptops
# ) t
# GROUP BY t.buckets
# ORDER BY MIN(Price);

# SELECT Company,COUNT(Company) FROM laptops
# GROUP BY Company;

# SELECT cpu_speed,Price FROM laptops;

# SELECT * FROM laptops;

# SELECT Company,
# SUM(CASE WHEN Touchscreen = 1 THEN 1 ELSE 0 END) AS 'Touchscreen_yes',
# SUM(CASE WHEN Touchscreen = 0 THEN 1 ELSE 0 END) AS 'Touchscreen_no'
# FROM laptops
# GROUP BY Company;

# SELECT DISTINCT cpu_brand FROM laptops;

# SELECT Company,
# SUM(CASE WHEN cpu_brand = 'Intel' THEN 1 ELSE 0 END) AS 'intel',
# SUM(CASE WHEN cpu_brand = 'AMD' THEN 1 ELSE 0 END) AS 'amd',
# SUM(CASE WHEN cpu_brand = 'Samsung' THEN 1 ELSE 0 END) AS 'samsung'
# FROM laptops
# GROUP BY Company;



# SELECT gpu_brand,
# CASE WHEN gpu_brand = 'Intel' THEN 1 ELSE 0 END AS 'intel',
# CASE WHEN gpu_brand = 'AMD' THEN 1 ELSE 0 END AS 'amd',
# CASE WHEN gpu_brand = 'nvidia' THEN 1 ELSE 0 END AS 'nvidia',
# CASE WHEN gpu_brand = 'arm' THEN 1 ELSE 0 END AS 'arm'
# FROM laptops

# ALTER TABLE laptops ADD COLUMN screen_size VARCHAR(255) AFTER Inches;

# UPDATE laptops
# SET screen_size = 
# CASE 
# 	WHEN Inches < 14.0 THEN 'small'
#     WHEN Inches >= 14.0 AND Inches < 17.0 THEN 'medium'
# 	ELSE 'large'
# END;

# SELECT screen_size,AVG(price) FROM laptops
# GROUP BY screen_size;

# select * from laptops;

# ALTER TABLE laptops ADD COLUMN ppi INTEGER;

# UPDATE laptops
# SET ppi = ROUND(SQRT(resolution_width*resolution_width + resolution_height*resolution_height)/Inches);

# SELECT * FROM laptops
# ORDER BY ppi DESC;

# UPDATE laptops l1
# SET price = (SELECT AVG(price) FROM laptops l2 WHERE
# 			 l2.Company = l1.Company)
# WHERE price IS NULL;
