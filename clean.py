# use laptops;
# select * from laptopdata;

# select distinct(Company) from laptopdata;

# select distinct(TypeName) from laptopdata;

# select distinct(Inches) from laptopdata;

# SELECT 
#     Inches,
#     CASE
#         WHEN Inches < 14 THEN 'SMALL'
#         WHEN Inches BETWEEN 14 AND 15.6 THEN 'MEDIUM'
#         WHEN Inches BETWEEN 15.7 AND 17 THEN 'LARGE'
#         WHEN Inches > 17 THEN 'EXTRA LARGE'
#     END AS ScreenSizeCategory
# FROM laptopdata;

# alter table laptopdata add column ScreenSizeCategory varchar(255) after Inches;
# select * from laptopdata;


# SET SQL_SAFE_UPDATES = 0;
# SET SQL_SAFE_UPDATES = 0;

# UPDATE laptopdata l1
# SET l1.ScreenSizeCategory = CASE
#     WHEN l1.Inches < 14 THEN 'SMALL'
#     WHEN l1.Inches BETWEEN 14 AND 15.6 THEN 'MEDIUM'
#     WHEN l1.Inches BETWEEN 15.7 AND 17 THEN 'LARGE'
#     WHEN l1.Inches > 17 THEN 'EXTRA LARGE'
# END;

# SET SQL_SAFE_UPDATES = 1;  -- (Optional) re-enable it after

# DELETE FROM laptopdata
# WHERE Weight = '?';


# select distinct((Weight)) from laptopdata;

# update laptopdata l1  set l1.Price = (select distinct(round(Price)));

# select * from laptopdata;

# update laptopdata set Weight = (select substring_index(Weight,"kg",1) as new_weight);

# UPDATE laptopdata
# SET Ram = Ram / 1024
# WHERE Ram IN (1024, 2048, 3072, 4096);



# select distinct((Ram)) from laptopdata;

# update laptopdata set Ram = (select substring_index(Ram,"GB",1));


# select distinct((OpSys)) from laptopdata;

#  update laptopdata set OpSys = (select substring_index(Opsys," ",1));
 
 
#  update laptopdata set OpSys = "NO OS" where Opsys = "No";



# use laptops;

# SELECT * FROM laptops;

# select distinct(Cpu) from laptopdata;

# SELECT DATA_LENGTH/1024 FROM information_schema.TABLES
# WHERE TABLE_SCHEMA = 'laptops'
# AND TABLE_NAME = 'laptopdata';


# ----  ALTER TABLE laptopdata DROP COLUMN `Unnamed: 0`;

# -- -- -- DELETE FROM laptopdata 
# -- -- -- WHERE `index` IN (SELECT `index` FROM laptopdata
# -- -- -- WHERE Company IS NULL AND TypeName IS NULL AND Inches IS NULL
# -- -- -- AND ScreenResolution IS NULL AND Cpu IS NULL AND Ram IS NULL
# -- -- -- AND Memory IS NULL AND Gpu IS NULL AND OpSys IS NULL AND
# -- -- WEIGHT IS NULL AND Price IS NULL)

# CREATE TABLE laptops LIKE laptopdata;

# INSERT INTO laptops
# SELECT * FROM laptops;

# ALTER TABLE laptops
# ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;

# SELECT * FROM laptops;


# DELETE FROM laptops 
# WHERE `id` IN (SELECT `id` 
# WHERE Company IS NULL AND TypeName IS NULL AND Inches IS NULL
# AND ScreenResolution IS NULL AND Cpu IS NULL AND Ram IS NULL
# AND Memory IS NULL AND Gpu IS NULL AND OpSys IS NULL AND
# WEIGHT IS NULL AND Price IS NULL);

# alter table laptops add column Gpu_Name varchar(255) after Gpu;

# alter table laptops add column Gpu_ varchar(255) after Gpu;

# alter table laptops add column Gpu_brand varchar(255) after Gpu;

# update laptops set Gpu_brand = (select substring_index(Gpu," ",1));

# select * from laptops;

# select distinct(Memory) from laptops;

 

# update laptops set Gpu_Name = (select replace(Gpu,Gpu_brand,""));

# ALTER TABLE laptops DROP COLUMN `Gpu`;
# ALTER TABLE laptops DROP COLUMN `Memory_Type`;

# ALTER  TABLE laptops add column Memory_Type varchar(255) after Memory; 

# ALTER  TABLE laptops add column Primary_Memory varchar(255) after Memory_type; 

# ALTER  TABLE laptops add column Secondary_Memory varchar(255) after Primary_Memory; 

# select Memory, substring_index(Memory," ",1) from laptops;

# update laptops set Primary_Memory = (select substring_index(Memory," ",1));

# select * from laptops;

# select distinct(replace(Memory,Primary_Memory,"")) from laptops;


# SELECT Memory,
# CASE
# 	WHEN Memory LIKE '%SSD%' AND Memory LIKE '%HDD%' THEN 'Hybrid'
#     WHEN Memory LIKE '%SSD%' THEN 'SSD'
#     WHEN Memory LIKE '%HDD%' THEN 'HDD'
#     WHEN Memory LIKE '%Flash Storage%' THEN 'Flash Storage'
#     WHEN Memory LIKE '%Hybrid%' THEN 'Hybrid'
#     WHEN Memory LIKE '%Flash Storage%' AND Memory LIKE '%HDD%' THEN 'Hybrid'
#     ELSE NULL
# END AS 'memory_type'
# FROM laptops;


# update laptops set Memory_Type = 
# (SELECT 
# CASE
# 	WHEN Memory LIKE '%SSD%' AND Memory LIKE '%HDD%' THEN 'Hybrid'
#     WHEN Memory LIKE '%SSD%' THEN 'SSD'
#     WHEN Memory LIKE '%HDD%' THEN 'HDD'
#     WHEN Memory LIKE '%Flash Storage%' THEN 'Flash Storage'
#     WHEN Memory LIKE '%Hybrid%' THEN 'Hybrid'
#     WHEN Memory LIKE '%Flash Storage%' AND Memory LIKE '%HDD%' THEN 'Hybrid'
#     ELSE NULL
# END );

# select * from laptops;

# UPDATE laptops
# SET Primary_Memory = REGEXP_SUBSTR(Primary_Memory,'[0-9]+');

# update laptops set Secondary_Memory = 
# (select
# case
#  when Memory like "%+%" then REGEXP_SUBSTR(SUBSTRING_INDEX(Memory,'+',-1),'[0-9]+') ELSE 0 END);
 
#  update laptops set Primary_Memory = 
#  (SELECT 
# CASE WHEN Primary_Memory <= 2 THEN Primary_Memory*1024 ELSE Primary_Memory END);

 
#  update laptops set Secondary_Memory = (select
# CASE WHEN Secondary_Memory <= 2 THEN Secondary_Memory*1024 ELSE Secondary_Memory END);

# select * from laptops;

# ALTER TABLE laptops DROP COLUMN `Memory`;


# ALTER TABLE laptops
# ADD COLUMN cpu_brand VARCHAR(255) AFTER Cpu,
# ADD COLUMN cpu_name VARCHAR(255) AFTER cpu_brand,
# ADD COLUMN cpu_speed DECIMAL(10,1) AFTER cpu_name;

# select Cpu, substring_index(Cpu," ",1) from laptops;

# update laptops set cpu_brand = (select substring_index(Cpu," ",1));

# select cpu, replace(substring_index(Cpu," ",-1),"GHz","") from laptops;

# update laptops set cpu_speed = (select replace(substring_index(Cpu," ",-1),"GHz","") );

# select * from laptops;

# SELECT 
#     Cpu,
#     replace(replace(replace(SUBSTRING_INDEX(Cpu, ' ', -4),cpu_speed,""),"GHz",""),"Intel","")AS cpu_model
# FROM laptops;

# update laptops set cpu_name = (SELECT
#     replace(replace(replace(SUBSTRING_INDEX(Cpu, ' ', -4),cpu_speed,""),"GHz",""),"Intel",""));

# ALTER TABLE laptops 
# ADD COLUMN resolution_width INTEGER AFTER ScreenResolution,
# ADD COLUMN resolution_height INTEGER AFTER resolution_width;

# SELECT * FROM laptops;

# UPDATE laptops
# SET resolution_width = SUBSTRING_INDEX(SUBSTRING_INDEX(ScreenResolution,' ',-1),'x',1),
# resolution_height = SUBSTRING_INDEX(SUBSTRING_INDEX(ScreenResolution,' ',-1),'x',-1);

# ALTER TABLE laptops 
# ADD COLUMN touchscreen INTEGER AFTER resolution_height;

# ALTER TABLE laptops 
# ADD COLUMN IPS_Panel INTEGER AFTER resolution_height;


# ALTER TABLE laptops 
# ADD COLUMN Full_HD INTEGER AFTER resolution_height;

# SELECT ScreenResolution LIKE '%Touch%' FROM laptops;

# UPDATE laptops
# SET touchscreen = ScreenResolution LIKE '%Touch%';

# UPDATE laptops
# SET IPS_Panel = ScreenResolution LIKE '%IPS%';


# UPDATE laptops
# SET Full_HD = ScreenResolution LIKE '%Full%';

# select * from laptops;

# alter table laptops drop column `ScreenResolution`;



