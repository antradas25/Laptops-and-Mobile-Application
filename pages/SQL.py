

import pymysql
from pymysql import Error

class DB:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="bzd0ukpckhpgzbo1f6w9-mysql.services.clever-cloud.com",
                user="uzjqi9fmpbwhdkky",
                password="2NSrCLcU3SeS1Yh6KTXg",
                database="bzd0ukpckhpgzbo1f6w9",
                port=3306
            )
            self.cursor = self.conn.cursor()
            print("[OK] Connection Established")
        except Error as e:
            print("[ERROR] Connection Error:", e)

    def migrate(self):
        queries = [
            # 1️⃣ Drop bad rows
            "DELETE FROM laptops WHERE Weight = '?'",
            
            # 2️⃣ Clean RAM
            "UPDATE laptops SET Ram = SUBSTRING_INDEX(Ram, 'GB', 1)",
            """UPDATE laptops 
               SET Ram = CASE 
                            WHEN Ram IN (1,2,3,4) THEN Ram*1024 
                            ELSE Ram 
                         END""",

            # 3️⃣ Clean Weight
            "UPDATE laptops SET Weight = SUBSTRING_INDEX(Weight, 'kg', 1)",

            # 4️⃣ Normalize OpSys
            "UPDATE laptops SET OpSys = SUBSTRING_INDEX(OpSys, ' ', 1)",
            "UPDATE laptops SET OpSys = 'No OS' WHERE OpSys = 'No'",

            # 5️⃣ Add Screen Size Category
            "ALTER TABLE laptops ADD COLUMN ScreenSizeCategory VARCHAR(255) AFTER Inches",
            """UPDATE laptops
               SET ScreenSizeCategory = CASE
                   WHEN Inches < 14 THEN 'SMALL'
                   WHEN Inches BETWEEN 14 AND 15.6 THEN 'MEDIUM'
                   WHEN Inches BETWEEN 15.7 AND 17 THEN 'LARGE'
                   WHEN Inches > 17 THEN 'EXTRA LARGE'
               END""",

            # # 7️⃣ GPU cleanup
            # "ALTER TABLE laptops ADD COLUMN Gpu_brand VARCHAR(255) AFTER Gpu",
            # "ALTER TABLE laptops ADD COLUMN Gpu_name VARCHAR(255) AFTER Gpu",
            # "UPDATE laptops SET Gpu_brand = SUBSTRING_INDEX(Gpu, ' ', 1)",
            # "UPDATE laptops SET Gpu_name = REPLACE(Gpu, Gpu_brand, '')",
            # "ALTER TABLE laptops DROP COLUMN Gpu",

            # # 8️⃣ Memory cleanup
            # "ALTER TABLE laptops ADD COLUMN Memory_Type VARCHAR(255) AFTER Memory",
            # "ALTER TABLE laptops ADD COLUMN Primary_Memory VARCHAR(255) AFTER Memory_Type",
            # "ALTER TABLE laptops ADD COLUMN Secondary_Memory VARCHAR(255) AFTER Primary_Memory",
            # """UPDATE laptops SET Memory_Type = CASE
            #     WHEN Memory LIKE '%SSD%' AND Memory LIKE '%HDD%' THEN 'Hybrid'
            #     WHEN Memory LIKE '%SSD%' THEN 'SSD'
            #     WHEN Memory LIKE '%HDD%' THEN 'HDD'
            #     WHEN Memory LIKE '%Flash Storage%' THEN 'Flash Storage'
            #     ELSE NULL
            # END""",
            # "UPDATE laptops SET Primary_Memory = REGEXP_SUBSTR(Memory, '^[0-9]+')",
            # """UPDATE laptops
            #    SET Secondary_Memory = CASE
            #        WHEN Memory LIKE '%+%' THEN REGEXP_SUBSTR(SUBSTRING_INDEX(Memory, '+', -1), '[0-9]+')
            #        ELSE 0 END""",
            # """UPDATE laptops
            #    SET Primary_Memory = CASE WHEN Primary_Memory <= 2 THEN Primary_Memory*1024 ELSE Primary_Memory END""",
            # """UPDATE laptops
            #    SET Secondary_Memory = CASE WHEN Secondary_Memory <= 2 THEN Secondary_Memory*1024 ELSE Secondary_Memory END""",
            # "ALTER TABLE laptops DROP COLUMN Memory",

            # # 9️⃣ CPU cleanup
            # "ALTER TABLE laptops ADD COLUMN cpu_brand VARCHAR(255) AFTER Cpu",
            # "ALTER TABLE laptops ADD COLUMN cpu_name VARCHAR(255) AFTER cpu_brand",
            # "ALTER TABLE laptops ADD COLUMN cpu_speed DECIMAL(10,2) AFTER cpu_name",
            # "UPDATE laptops SET cpu_brand = SUBSTRING_INDEX(Cpu, ' ', 1)",
            # "UPDATE laptops SET cpu_speed = REPLACE(SUBSTRING_INDEX(Cpu, ' ', -1), 'GHz', '')",
            # """UPDATE laptops SET cpu_name = TRIM(
            #        REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(Cpu, ' ', -4), cpu_speed, ''), 'GHz', ''), 'Intel', '')
            #    )""",

            # # 🔟 Screen Resolution cleanup
            # "ALTER TABLE laptops ADD COLUMN resolution_width INT AFTER ScreenResolution",
            # "ALTER TABLE laptops ADD COLUMN resolution_height INT AFTER resolution_width",
            # "ALTER TABLE laptops ADD COLUMN touchscreen BOOLEAN AFTER resolution_height",
            # "ALTER TABLE laptops ADD COLUMN IPS_Panel BOOLEAN AFTER touchscreen",
            # "ALTER TABLE laptops ADD COLUMN Full_HD BOOLEAN AFTER IPS_Panel",
            # """UPDATE laptops
            #    SET resolution_width = SUBSTRING_INDEX(SUBSTRING_INDEX(ScreenResolution, ' ', -1), 'x', 1),
            #        resolution_height = SUBSTRING_INDEX(SUBSTRING_INDEX(ScreenResolution, ' ', -1), 'x', -1)""",
            # "UPDATE laptops SET touchscreen = ScreenResolution LIKE '%Touch%'",
            # "UPDATE laptops SET IPS_Panel = ScreenResolution LIKE '%IPS%'",
            # "UPDATE laptops SET Full_HD = ScreenResolution LIKE '%Full%'",
            # "ALTER TABLE laptops DROP COLUMN ScreenResolution"
        ]

        for query in queries:
            try:
                self.cursor.execute(query)
                self.conn.commit()
                print(f"[OK] Executed: {query}")
            except Exception as e:
                print(f"[WARNING] Error running query: {query}\n   {e}")

        print("[DONE] Migration finished!")

# if __name__ == "__main__":
#     db = DB()
#     db.migrate()

    def new_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS laptops1;")
        self.conn.commit()
        self.cursor.execute("CREATE TABLE laptops1 AS SELECT * FROM laptops;")
        self.conn.commit()
        print("COPY CREATED")

    def OHE(self):
        queries = [
            # 1. Add columns for TypeName OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN Ultrabook TINYINT DEFAULT 0,
                ADD COLUMN Notebook TINYINT DEFAULT 0,
                ADD COLUMN Gaming TINYINT DEFAULT 0,
                ADD COLUMN Workstation TINYINT DEFAULT 0,
                ADD COLUMN Convertible TINYINT DEFAULT 0
            """,

            # 2. Update TypeName OHE
            """
            UPDATE laptops1
            SET 
                Ultrabook = CASE WHEN TypeName = 'Ultrabook' THEN 1 ELSE 0 END,
                Notebook = CASE WHEN TypeName = 'Notebook' THEN 1 ELSE 0 END,
                Gaming = CASE WHEN TypeName = 'Gaming' THEN 1 ELSE 0 END,
                Workstation = CASE WHEN TypeName = 'Workstation' THEN 1 ELSE 0 END,
                Convertible = CASE WHEN TypeName = 'Convertible' THEN 1 ELSE 0 END
            """,

            # 3. Add columns for Companies OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN is_Xiaomi INT,
                ADD COLUMN is_Vero INT,
                ADD COLUMN is_Toshiba INT,
                ADD COLUMN is_Samsung INT,
                ADD COLUMN is_Razer INT,
                ADD COLUMN is_MSI INT,
                ADD COLUMN is_Microsoft INT,
                ADD COLUMN is_Mediacom INT,
                ADD COLUMN is_LG INT,
                ADD COLUMN is_Lenovo INT,
                ADD COLUMN is_Huawei INT,
                ADD COLUMN is_HP INT,
                ADD COLUMN is_Google INT,
                ADD COLUMN is_Fujitsu INT,
                ADD COLUMN is_Dell INT,
                ADD COLUMN is_Chuwi INT,
                ADD COLUMN is_Asus INT,
                ADD COLUMN is_Apple INT,
                ADD COLUMN is_Acer INT
            """,

            # 4. Update Companies OHE
            """
            UPDATE laptops1 SET
                is_Xiaomi = CASE WHEN Company = 'Xiaomi' THEN 1 ELSE 0 END,
                is_Vero = CASE WHEN Company = 'Vero' THEN 1 ELSE 0 END,
                is_Toshiba = CASE WHEN Company = 'Toshiba' THEN 1 ELSE 0 END,
                is_Samsung = CASE WHEN Company = 'Samsung' THEN 1 ELSE 0 END,
                is_Razer = CASE WHEN Company = 'Razer' THEN 1 ELSE 0 END,
                is_MSI = CASE WHEN Company = 'MSI' THEN 1 ELSE 0 END,
                is_Microsoft = CASE WHEN Company = 'Microsoft' THEN 1 ELSE 0 END,
                is_Mediacom = CASE WHEN Company = 'Mediacom' THEN 1 ELSE 0 END,
                is_LG = CASE WHEN Company = 'LG' THEN 1 ELSE 0 END,
                is_Lenovo = CASE WHEN Company = 'Lenovo' THEN 1 ELSE 0 END,
                is_Huawei = CASE WHEN Company = 'Huawei' THEN 1 ELSE 0 END,
                is_HP = CASE WHEN Company = 'HP' THEN 1 ELSE 0 END,
                is_Google = CASE WHEN Company = 'Google' THEN 1 ELSE 0 END,
                is_Fujitsu = CASE WHEN Company = 'Fujitsu' THEN 1 ELSE 0 END,
                is_Dell = CASE WHEN Company = 'Dell' THEN 1 ELSE 0 END,
                is_Chuwi = CASE WHEN Company = 'Chuwi' THEN 1 ELSE 0 END,
                is_Asus = CASE WHEN Company = 'Asus' THEN 1 ELSE 0 END,
                is_Apple = CASE WHEN Company = 'Apple' THEN 1 ELSE 0 END,
                is_Acer = CASE WHEN Company = 'Acer' THEN 1 ELSE 0 END
            """,

            # 5. Drop Company and TypeName columns
            "ALTER TABLE laptops1 DROP COLUMN Company",
            "ALTER TABLE laptops1 DROP COLUMN TypeName",

            # 6. Add columns for ScreenSizeCategory OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN MEDIUM INT,
                ADD COLUMN SMALL INT,
                ADD COLUMN EXTRA_LARGE INT,
                ADD COLUMN LARGE INT
            """,

            # 7. Update ScreenSizeCategory OHE
            """
            UPDATE laptops1 SET
                SMALL = CASE WHEN ScreenSizeCategory = 'SMALL' THEN 1 ELSE 0 END,
                MEDIUM = CASE WHEN ScreenSizeCategory = 'MEDIUM' THEN 1 ELSE 0 END,
                LARGE = CASE WHEN ScreenSizeCategory = 'LARGE' THEN 1 ELSE 0 END,
                EXTRA_LARGE = CASE WHEN ScreenSizeCategory = 'EXTRA LARGE' THEN 1 ELSE 0 END
            """,

            # 8. Drop ScreenSizeCategory column
            "ALTER TABLE laptops1 DROP COLUMN ScreenSizeCategory",

            # 9. Drop Cpu and Gpu_Name columns
            "ALTER TABLE laptops1 DROP COLUMN Cpu",
            "ALTER TABLE laptops1 DROP COLUMN Gpu_Name",

            # 10. Add columns for cpu_brand OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN cpu_Intel INT,
                ADD COLUMN cpu_AMD INT,
                ADD COLUMN cpu_Samsung INT
            """,

            # 11. Update cpu_brand OHE
            """
            UPDATE laptops1 SET
                cpu_Intel = CASE WHEN cpu_brand = 'Intel' THEN 1 ELSE 0 END,
                cpu_AMD = CASE WHEN cpu_brand = 'AMD' THEN 1 ELSE 0 END,
                cpu_Samsung = CASE WHEN cpu_brand = 'Samsung' THEN 1 ELSE 0 END
            """,

            # 12. Drop cpu_name and cpu_brand columns
            "ALTER TABLE laptops1 DROP COLUMN cpu_name",
            "ALTER TABLE laptops1 DROP COLUMN cpu_brand",

            # 13. Add columns for Gpu_brand OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN gpu_Nvidia INT,
                ADD COLUMN gpu_Intel INT,
                ADD COLUMN gpu_AMD INT,
                ADD COLUMN gpu_ARM INT
            """,

            # 14. Update Gpu_brand OHE
            """
            UPDATE laptops1 SET
                gpu_Nvidia = CASE WHEN Gpu_brand = 'Nvidia' THEN 1 ELSE 0 END,
                gpu_Intel  = CASE WHEN Gpu_brand = 'Intel' THEN 1 ELSE 0 END,
                gpu_AMD    = CASE WHEN Gpu_brand = 'AMD' THEN 1 ELSE 0 END,
                gpu_ARM    = CASE WHEN Gpu_brand = 'ARM' THEN 1 ELSE 0 END
            """,

            # 15. Drop Gpu_brand column
            "ALTER TABLE laptops1 DROP COLUMN Gpu_brand",

            # 16. Add columns for Memory_Type OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN mem_SSD INT,
                ADD COLUMN mem_HDD INT,
                ADD COLUMN mem_Hybrid INT,
                ADD COLUMN mem_FlashStorage INT
            """,

            # 17. Update Memory_Type OHE
            """
            UPDATE laptops1 SET
                mem_SSD = CASE WHEN Memory_Type = 'SSD' THEN 1 ELSE 0 END,
                mem_HDD = CASE WHEN Memory_Type = 'HDD' THEN 1 ELSE 0 END,
                mem_Hybrid = CASE WHEN Memory_Type = 'Hybrid' THEN 1 ELSE 0 END,
                mem_FlashStorage = CASE WHEN Memory_Type = 'Flash Storage' THEN 1 ELSE 0 END
            """,

            # 18. Drop Memory_Type column
            "ALTER TABLE laptops1 DROP COLUMN Memory_Type",

            # 19. Add columns for OpSys OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN os_Windows INT,
                ADD COLUMN os_macOS INT,
                ADD COLUMN os_NOOS INT,
                ADD COLUMN os_Linux INT,
                ADD COLUMN os_Mac INT,
                ADD COLUMN os_Chrome INT,
                ADD COLUMN os_Android INT
            """,

            # 20. Update OpSys OHE
            """
            UPDATE laptops1 SET
                os_Windows = CASE WHEN OpSys = 'Windows' THEN 1 ELSE 0 END,
                os_macOS = CASE WHEN OpSys = 'macOS' THEN 1 ELSE 0 END,
                os_NOOS = CASE WHEN OpSys = 'No OS' THEN 1 ELSE 0 END,
                os_Linux = CASE WHEN OpSys = 'Linux' THEN 1 ELSE 0 END,
                os_Mac = CASE WHEN OpSys = 'Mac' THEN 1 ELSE 0 END,
                os_Chrome = CASE WHEN OpSys = 'Chrome' THEN 1 ELSE 0 END,
                os_Android = CASE WHEN OpSys = 'Android' THEN 1 ELSE 0 END
            """,

            # 21. Drop OpSys column
            "ALTER TABLE laptops1 DROP COLUMN OpSys"
        ]

        for query in queries:
            try:
                self.cursor.execute(query)
                self.conn.commit()
                print(f"[OK] Executed: {query.strip().splitlines()[0]} ...")  # Print only the first line of query
            except Exception as e:
                print(f"[WARNING] Error running query: {query.strip().splitlines()[0]} ...\n   {e}")

        print("[DONE] OHE finished!")


    def company_available(self):
        try:
            self.cursor.execute("SELECT DISTINCT Company FROM laptops ORDER BY Company")
            companies = [row[0] for row in self.cursor.fetchall()]
            return companies
        except Exception as e:
            print("[WARNING] Error fetching companies:", e)
            return []
        
    def Typename(self):
        try:
            self.cursor.execute("select distinct(TypeName) from laptops")
            typename = [row[0] for row in self.cursor.fetchall()]
            return typename
        except Exception as e:
            print("[WARNING] Error fetching Type:", e)
            return []
        
    def your_search(self, company, typename):
        try:
            query = """
                SELECT 
                    Company,
                    TypeName,
                    cpu_brand,
                    Ram,
                    Gpu_brand,
                    OpSys,
                    Price
                FROM laptops 
                WHERE Company = %s AND TypeName = %s
            """
            self.cursor.execute(query, (company, typename))
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]  
            return rows, columns
        except Exception as e:
            print("[WARNING] Error fetching Data:", e)
            return [], []
        
    def Inches(self):
        try:
            self.cursor.execute("SELECT DISTINCT Inches FROM laptops ORDER BY Inches")
            inches = [row[0] for row in self.cursor.fetchall()]
            return inches
        except Exception as e:
            print("[WARNING] Error fetching Inches:", e)
            return []

    def ScreenSizeCategory(self):
        try:
            self.cursor.execute("SELECT DISTINCT ScreenSizeCategory FROM laptops ORDER BY ScreenSizeCategory")
            category = [row[0] for row in self.cursor.fetchall()]
            return category
        except Exception as e:
            print("[WARNING] Error fetching ScreenSizeCategory:", e)
            return []

    def resolution_width(self):
        try:
            self.cursor.execute("SELECT DISTINCT resolution_width FROM laptops ORDER BY resolution_width")
            widths = [row[0] for row in self.cursor.fetchall()]
            return widths
        except Exception as e:
            print("[WARNING] Error fetching resolution_width:", e)
            return []

    def resolution_height(self):
        try:
            self.cursor.execute("SELECT DISTINCT resolution_height FROM laptops ORDER BY resolution_height")
            heights = [row[0] for row in self.cursor.fetchall()]
            return heights
        except Exception as e:
            print("[WARNING] Error fetching resolution_height:", e)
            return []

    def touchscreen(self):
        try:
            self.cursor.execute("SELECT DISTINCT touchscreen FROM laptops ORDER BY touchscreen")
            touchscreen_vals = [row[0] for row in self.cursor.fetchall()]
            return touchscreen_vals
        except Exception as e:
            print("[WARNING] Error fetching touchscreen:", e)
            return []

    def IPS_Panel(self):
        try:
            self.cursor.execute("SELECT DISTINCT IPS_Panel FROM laptops ORDER BY IPS_Panel")
            ips_vals = [row[0] for row in self.cursor.fetchall()]
            return ips_vals
        except Exception as e:
            print("[WARNING] Error fetching IPS_Panel:", e)
            return []

    def Full_HD(self):
        try:
            self.cursor.execute("SELECT DISTINCT Full_HD FROM laptops ORDER BY Full_HD")
            full_hd_vals = [row[0] for row in self.cursor.fetchall()]
            return full_hd_vals
        except Exception as e:
            print("[WARNING] Error fetching Full_HD:", e)
            return []

    def cpu_brand(self):
        try:
            self.cursor.execute("SELECT DISTINCT cpu_brand FROM laptops ORDER BY cpu_brand")
            brands = [row[0] for row in self.cursor.fetchall()]
            return brands
        except Exception as e:
            print("[WARNING] Error fetching cpu_brand:", e)
            return []

    def cpu_speed(self):
        try:
            self.cursor.execute("SELECT DISTINCT cpu_speed FROM laptops ORDER BY cpu_speed")
            speeds = [row[0] for row in self.cursor.fetchall()]
            return speeds
        except Exception as e:
            print("[WARNING] Error fetching cpu_speed:", e)
            return []

    def Ram(self):
        try:
            self.cursor.execute("SELECT DISTINCT Ram FROM laptops ORDER BY Ram")
            ram_vals = [row[0] for row in self.cursor.fetchall()]
            return ram_vals
        except Exception as e:
            print("[WARNING] Error fetching Ram:", e)
            return []

    def Memory_Type(self):
        try:
            self.cursor.execute("SELECT DISTINCT Memory_Type FROM laptops ORDER BY Memory_Type")
            mem_types = [row[0] for row in self.cursor.fetchall()]
            return mem_types
        except Exception as e:
            print("[WARNING] Error fetching Memory_Type:", e)
            return []

    def Primary_Memory(self):
        try:
            self.cursor.execute("SELECT DISTINCT Primary_Memory FROM laptops ORDER BY Primary_Memory")
            primary_mem = [row[0] for row in self.cursor.fetchall()]
            return primary_mem
        except Exception as e:
            print("[WARNING] Error fetching Primary_Memory:", e)
            return []

    def Secondary_Memory(self):
        try:
            self.cursor.execute("SELECT DISTINCT Secondary_Memory FROM laptops ORDER BY Secondary_Memory")
            secondary_mem = [row[0] for row in self.cursor.fetchall()]
            return secondary_mem
        except Exception as e:
            print("[WARNING] Error fetching Secondary_Memory:", e)
            return []

    def Gpu_brand(self):
        try:
            self.cursor.execute("SELECT DISTINCT Gpu_brand FROM laptops ORDER BY Gpu_brand")
            gpu_brands = [row[0] for row in self.cursor.fetchall()]
            return gpu_brands
        except Exception as e:
            print("[WARNING] Error fetching Gpu_brand:", e)
            return []

    def OpSys(self):
        try:
            self.cursor.execute("SELECT DISTINCT OpSys FROM laptops ORDER BY OpSys")
            opsys_vals = [row[0] for row in self.cursor.fetchall()]
            return opsys_vals
        except Exception as e:
            print("[WARNING] Error fetching OpSys:", e)
            return []

    def Weight(self):
        try:
            self.cursor.execute("SELECT DISTINCT Weight FROM laptops ORDER BY Weight")
            weights = [row[0] for row in self.cursor.fetchall()]
            return weights
        except Exception as e:
            print("[WARNING] Error fetching Weight:", e)
            return []



    

        
if __name__ == "__main__":
    db = DB()
    db.migrate()
    db.new_table()
    db.OHE()


import streamlit as st 

code = '''import pymysql
from pymysql import Error

class DB:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="bzd0ukpckhpgzbo1f6w9-mysql.services.clever-cloud.com",
                user="uzjqi9fmpbwhdkky",
                password="2NSrCLcU3SeS1Yh6KTXg",
                database="bzd0ukpckhpgzbo1f6w9",
                port=3306
            )
            self.cursor = self.conn.cursor()
            print("[OK] Connection Established")
        except Error as e:
            print("[ERROR] Connection Error:", e)

    def migrate(self):
        queries = [
            # 1️⃣ Drop bad rows
            "DELETE FROM laptops WHERE Weight = '?'",
            
            # 2️⃣ Clean RAM
            "UPDATE laptops SET Ram = SUBSTRING_INDEX(Ram, 'GB', 1)",
            """UPDATE laptops 
               SET Ram = CASE 
                            WHEN Ram IN (1,2,3,4) THEN Ram*1024 
                            ELSE Ram 
                         END""",

            # 3️⃣ Clean Weight
            "UPDATE laptops SET Weight = SUBSTRING_INDEX(Weight, 'kg', 1)",

            # 4️⃣ Normalize OpSys
            "UPDATE laptops SET OpSys = SUBSTRING_INDEX(OpSys, ' ', 1)",
            "UPDATE laptops SET OpSys = 'No OS' WHERE OpSys = 'No'",

            # 5️⃣ Add Screen Size Category
            "ALTER TABLE laptops ADD COLUMN ScreenSizeCategory VARCHAR(255) AFTER Inches",
            """UPDATE laptops
               SET ScreenSizeCategory = CASE
                   WHEN Inches < 14 THEN 'SMALL'
                   WHEN Inches BETWEEN 14 AND 15.6 THEN 'MEDIUM'
                   WHEN Inches BETWEEN 15.7 AND 17 THEN 'LARGE'
                   WHEN Inches > 17 THEN 'EXTRA LARGE'
               END""",

            # # 7️⃣ GPU cleanup
            # "ALTER TABLE laptops ADD COLUMN Gpu_brand VARCHAR(255) AFTER Gpu",
            # "ALTER TABLE laptops ADD COLUMN Gpu_name VARCHAR(255) AFTER Gpu",
            # "UPDATE laptops SET Gpu_brand = SUBSTRING_INDEX(Gpu, ' ', 1)",
            # "UPDATE laptops SET Gpu_name = REPLACE(Gpu, Gpu_brand, '')",
            # "ALTER TABLE laptops DROP COLUMN Gpu",

            # # 8️⃣ Memory cleanup
            # "ALTER TABLE laptops ADD COLUMN Memory_Type VARCHAR(255) AFTER Memory",
            # "ALTER TABLE laptops ADD COLUMN Primary_Memory VARCHAR(255) AFTER Memory_Type",
            # "ALTER TABLE laptops ADD COLUMN Secondary_Memory VARCHAR(255) AFTER Primary_Memory",
            # """UPDATE laptops SET Memory_Type = CASE
            #     WHEN Memory LIKE '%SSD%' AND Memory LIKE '%HDD%' THEN 'Hybrid'
            #     WHEN Memory LIKE '%SSD%' THEN 'SSD'
            #     WHEN Memory LIKE '%HDD%' THEN 'HDD'
            #     WHEN Memory LIKE '%Flash Storage%' THEN 'Flash Storage'
            #     ELSE NULL
            # END""",
            # "UPDATE laptops SET Primary_Memory = REGEXP_SUBSTR(Memory, '^[0-9]+')",
            # """UPDATE laptops
            #    SET Secondary_Memory = CASE
            #        WHEN Memory LIKE '%+%' THEN REGEXP_SUBSTR(SUBSTRING_INDEX(Memory, '+', -1), '[0-9]+')
            #        ELSE 0 END""",
            # """UPDATE laptops
            #    SET Primary_Memory = CASE WHEN Primary_Memory <= 2 THEN Primary_Memory*1024 ELSE Primary_Memory END""",
            # """UPDATE laptops
            #    SET Secondary_Memory = CASE WHEN Secondary_Memory <= 2 THEN Secondary_Memory*1024 ELSE Secondary_Memory END""",
            # "ALTER TABLE laptops DROP COLUMN Memory",

            # # 9️⃣ CPU cleanup
            # "ALTER TABLE laptops ADD COLUMN cpu_brand VARCHAR(255) AFTER Cpu",
            # "ALTER TABLE laptops ADD COLUMN cpu_name VARCHAR(255) AFTER cpu_brand",
            # "ALTER TABLE laptops ADD COLUMN cpu_speed DECIMAL(10,2) AFTER cpu_name",
            # "UPDATE laptops SET cpu_brand = SUBSTRING_INDEX(Cpu, ' ', 1)",
            # "UPDATE laptops SET cpu_speed = REPLACE(SUBSTRING_INDEX(Cpu, ' ', -1), 'GHz', '')",
            # """UPDATE laptops SET cpu_name = TRIM(
            #        REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(Cpu, ' ', -4), cpu_speed, ''), 'GHz', ''), 'Intel', '')
            #    )""",

            # # 🔟 Screen Resolution cleanup
            # "ALTER TABLE laptops ADD COLUMN resolution_width INT AFTER ScreenResolution",
            # "ALTER TABLE laptops ADD COLUMN resolution_height INT AFTER resolution_width",
            # "ALTER TABLE laptops ADD COLUMN touchscreen BOOLEAN AFTER resolution_height",
            # "ALTER TABLE laptops ADD COLUMN IPS_Panel BOOLEAN AFTER touchscreen",
            # "ALTER TABLE laptops ADD COLUMN Full_HD BOOLEAN AFTER IPS_Panel",
            # """UPDATE laptops
            #    SET resolution_width = SUBSTRING_INDEX(SUBSTRING_INDEX(ScreenResolution, ' ', -1), 'x', 1),
            #        resolution_height = SUBSTRING_INDEX(SUBSTRING_INDEX(ScreenResolution, ' ', -1), 'x', -1)""",
            # "UPDATE laptops SET touchscreen = ScreenResolution LIKE '%Touch%'",
            # "UPDATE laptops SET IPS_Panel = ScreenResolution LIKE '%IPS%'",
            # "UPDATE laptops SET Full_HD = ScreenResolution LIKE '%Full%'",
            # "ALTER TABLE laptops DROP COLUMN ScreenResolution"
        ]

        for query in queries:
            try:
                self.cursor.execute(query)
                self.conn.commit()
                print(f"[OK] Executed: {query}")
            except Exception as e:
                print(f"[WARNING] Error running query: {query}\n   {e}")

        print("[DONE] Migration finished!")

# if __name__ == "__main__":
#     db = DB()
#     db.migrate()

    def new_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS laptops1;")
        self.conn.commit()
        self.cursor.execute("CREATE TABLE laptops1 AS SELECT * FROM laptops;")
        self.conn.commit()
        print("COPY CREATED")

    def OHE(self):
        queries = [
            # 1. Add columns for TypeName OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN Ultrabook TINYINT DEFAULT 0,
                ADD COLUMN Notebook TINYINT DEFAULT 0,
                ADD COLUMN Gaming TINYINT DEFAULT 0,
                ADD COLUMN Workstation TINYINT DEFAULT 0,
                ADD COLUMN Convertible TINYINT DEFAULT 0
            """,

            # 2. Update TypeName OHE
            """
            UPDATE laptops1
            SET 
                Ultrabook = CASE WHEN TypeName = 'Ultrabook' THEN 1 ELSE 0 END,
                Notebook = CASE WHEN TypeName = 'Notebook' THEN 1 ELSE 0 END,
                Gaming = CASE WHEN TypeName = 'Gaming' THEN 1 ELSE 0 END,
                Workstation = CASE WHEN TypeName = 'Workstation' THEN 1 ELSE 0 END,
                Convertible = CASE WHEN TypeName = 'Convertible' THEN 1 ELSE 0 END
            """,

            # 3. Add columns for Companies OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN is_Xiaomi INT,
                ADD COLUMN is_Vero INT,
                ADD COLUMN is_Toshiba INT,
                ADD COLUMN is_Samsung INT,
                ADD COLUMN is_Razer INT,
                ADD COLUMN is_MSI INT,
                ADD COLUMN is_Microsoft INT,
                ADD COLUMN is_Mediacom INT,
                ADD COLUMN is_LG INT,
                ADD COLUMN is_Lenovo INT,
                ADD COLUMN is_Huawei INT,
                ADD COLUMN is_HP INT,
                ADD COLUMN is_Google INT,
                ADD COLUMN is_Fujitsu INT,
                ADD COLUMN is_Dell INT,
                ADD COLUMN is_Chuwi INT,
                ADD COLUMN is_Asus INT,
                ADD COLUMN is_Apple INT,
                ADD COLUMN is_Acer INT
            """,

            # 4. Update Companies OHE
            """
            UPDATE laptops1 SET
                is_Xiaomi = CASE WHEN Company = 'Xiaomi' THEN 1 ELSE 0 END,
                is_Vero = CASE WHEN Company = 'Vero' THEN 1 ELSE 0 END,
                is_Toshiba = CASE WHEN Company = 'Toshiba' THEN 1 ELSE 0 END,
                is_Samsung = CASE WHEN Company = 'Samsung' THEN 1 ELSE 0 END,
                is_Razer = CASE WHEN Company = 'Razer' THEN 1 ELSE 0 END,
                is_MSI = CASE WHEN Company = 'MSI' THEN 1 ELSE 0 END,
                is_Microsoft = CASE WHEN Company = 'Microsoft' THEN 1 ELSE 0 END,
                is_Mediacom = CASE WHEN Company = 'Mediacom' THEN 1 ELSE 0 END,
                is_LG = CASE WHEN Company = 'LG' THEN 1 ELSE 0 END,
                is_Lenovo = CASE WHEN Company = 'Lenovo' THEN 1 ELSE 0 END,
                is_Huawei = CASE WHEN Company = 'Huawei' THEN 1 ELSE 0 END,
                is_HP = CASE WHEN Company = 'HP' THEN 1 ELSE 0 END,
                is_Google = CASE WHEN Company = 'Google' THEN 1 ELSE 0 END,
                is_Fujitsu = CASE WHEN Company = 'Fujitsu' THEN 1 ELSE 0 END,
                is_Dell = CASE WHEN Company = 'Dell' THEN 1 ELSE 0 END,
                is_Chuwi = CASE WHEN Company = 'Chuwi' THEN 1 ELSE 0 END,
                is_Asus = CASE WHEN Company = 'Asus' THEN 1 ELSE 0 END,
                is_Apple = CASE WHEN Company = 'Apple' THEN 1 ELSE 0 END,
                is_Acer = CASE WHEN Company = 'Acer' THEN 1 ELSE 0 END
            """,

            # 5. Drop Company and TypeName columns
            "ALTER TABLE laptops1 DROP COLUMN Company",
            "ALTER TABLE laptops1 DROP COLUMN TypeName",

            # 6. Add columns for ScreenSizeCategory OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN MEDIUM INT,
                ADD COLUMN SMALL INT,
                ADD COLUMN EXTRA_LARGE INT,
                ADD COLUMN LARGE INT
            """,

            # 7. Update ScreenSizeCategory OHE
            """
            UPDATE laptops1 SET
                SMALL = CASE WHEN ScreenSizeCategory = 'SMALL' THEN 1 ELSE 0 END,
                MEDIUM = CASE WHEN ScreenSizeCategory = 'MEDIUM' THEN 1 ELSE 0 END,
                LARGE = CASE WHEN ScreenSizeCategory = 'LARGE' THEN 1 ELSE 0 END,
                EXTRA_LARGE = CASE WHEN ScreenSizeCategory = 'EXTRA LARGE' THEN 1 ELSE 0 END
            """,

            # 8. Drop ScreenSizeCategory column
            "ALTER TABLE laptops1 DROP COLUMN ScreenSizeCategory",

            # 9. Drop Cpu and Gpu_Name columns
            "ALTER TABLE laptops1 DROP COLUMN Cpu",
            "ALTER TABLE laptops1 DROP COLUMN Gpu_Name",

            # 10. Add columns for cpu_brand OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN cpu_Intel INT,
                ADD COLUMN cpu_AMD INT,
                ADD COLUMN cpu_Samsung INT
            """,

            # 11. Update cpu_brand OHE
            """
            UPDATE laptops1 SET
                cpu_Intel = CASE WHEN cpu_brand = 'Intel' THEN 1 ELSE 0 END,
                cpu_AMD = CASE WHEN cpu_brand = 'AMD' THEN 1 ELSE 0 END,
                cpu_Samsung = CASE WHEN cpu_brand = 'Samsung' THEN 1 ELSE 0 END
            """,

            # 12. Drop cpu_name and cpu_brand columns
            "ALTER TABLE laptops1 DROP COLUMN cpu_name",
            "ALTER TABLE laptops1 DROP COLUMN cpu_brand",

            # 13. Add columns for Gpu_brand OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN gpu_Nvidia INT,
                ADD COLUMN gpu_Intel INT,
                ADD COLUMN gpu_AMD INT,
                ADD COLUMN gpu_ARM INT
            """,

            # 14. Update Gpu_brand OHE
            """
            UPDATE laptops1 SET
                gpu_Nvidia = CASE WHEN Gpu_brand = 'Nvidia' THEN 1 ELSE 0 END,
                gpu_Intel  = CASE WHEN Gpu_brand = 'Intel' THEN 1 ELSE 0 END,
                gpu_AMD    = CASE WHEN Gpu_brand = 'AMD' THEN 1 ELSE 0 END,
                gpu_ARM    = CASE WHEN Gpu_brand = 'ARM' THEN 1 ELSE 0 END
            """,

            # 15. Drop Gpu_brand column
            "ALTER TABLE laptops1 DROP COLUMN Gpu_brand",

            # 16. Add columns for Memory_Type OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN mem_SSD INT,
                ADD COLUMN mem_HDD INT,
                ADD COLUMN mem_Hybrid INT,
                ADD COLUMN mem_FlashStorage INT
            """,

            # 17. Update Memory_Type OHE
            """
            UPDATE laptops1 SET
                mem_SSD = CASE WHEN Memory_Type = 'SSD' THEN 1 ELSE 0 END,
                mem_HDD = CASE WHEN Memory_Type = 'HDD' THEN 1 ELSE 0 END,
                mem_Hybrid = CASE WHEN Memory_Type = 'Hybrid' THEN 1 ELSE 0 END,
                mem_FlashStorage = CASE WHEN Memory_Type = 'Flash Storage' THEN 1 ELSE 0 END
            """,

            # 18. Drop Memory_Type column
            "ALTER TABLE laptops1 DROP COLUMN Memory_Type",

            # 19. Add columns for OpSys OHE
            """
            ALTER TABLE laptops1
                ADD COLUMN os_Windows INT,
                ADD COLUMN os_macOS INT,
                ADD COLUMN os_NOOS INT,
                ADD COLUMN os_Linux INT,
                ADD COLUMN os_Mac INT,
                ADD COLUMN os_Chrome INT,
                ADD COLUMN os_Android INT
            """,

            # 20. Update OpSys OHE
            """
            UPDATE laptops1 SET
                os_Windows = CASE WHEN OpSys = 'Windows' THEN 1 ELSE 0 END,
                os_macOS = CASE WHEN OpSys = 'macOS' THEN 1 ELSE 0 END,
                os_NOOS = CASE WHEN OpSys = 'No OS' THEN 1 ELSE 0 END,
                os_Linux = CASE WHEN OpSys = 'Linux' THEN 1 ELSE 0 END,
                os_Mac = CASE WHEN OpSys = 'Mac' THEN 1 ELSE 0 END,
                os_Chrome = CASE WHEN OpSys = 'Chrome' THEN 1 ELSE 0 END,
                os_Android = CASE WHEN OpSys = 'Android' THEN 1 ELSE 0 END
            """,

            # 21. Drop OpSys column
            "ALTER TABLE laptops1 DROP COLUMN OpSys"
        ]

        for query in queries:
            try:
                self.cursor.execute(query)
                self.conn.commit()
                print(f"[OK] Executed: {query.strip().splitlines()[0]} ...")  # Print only the first line of query
            except Exception as e:
                print(f"[WARNING] Error running query: {query.strip().splitlines()[0]} ...\n   {e}")

        print("[OK] OHE finished!")


    def company_available(self):
        try:
            self.cursor.execute("SELECT DISTINCT Company FROM laptops ORDER BY Company")
            companies = [row[0] for row in self.cursor.fetchall()]
            return companies
        except Exception as e:
            print("⚠️ Error fetching companies:", e)
            return []
        
    def Typename(self):
        try:
            self.cursor.execute("select distinct(TypeName) from laptops")
            typename = [row[0] for row in self.cursor.fetchall()]
            return typename
        except Exception as e:
            print("⚠️ Error fetching Type:", e)
            return []
        
    def your_search(self, company, typename):
        try:
            query = """
                SELECT 
                    Company,
                    TypeName,
                    cpu_brand,
                    Ram,
                    Gpu_brand,
                    OpSys,
                    Price
                FROM laptops 
                WHERE Company = %s AND TypeName = %s
            """
            self.cursor.execute(query, (company, typename))
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]  
            return rows, columns
        except Exception as e:
            print("⚠️ Error fetching Data:", e)
            return [], []
        
    def Inches(self):
        try:
            self.cursor.execute("SELECT DISTINCT Inches FROM laptops ORDER BY Inches")
            inches = [row[0] for row in self.cursor.fetchall()]
            return inches
        except Exception as e:
            print("⚠️ Error fetching Inches:", e)
            return []

    def ScreenSizeCategory(self):
        try:
            self.cursor.execute("SELECT DISTINCT ScreenSizeCategory FROM laptops ORDER BY ScreenSizeCategory")
            category = [row[0] for row in self.cursor.fetchall()]
            return category
        except Exception as e:
            print("⚠️ Error fetching ScreenSizeCategory:", e)
            return []

    def resolution_width(self):
        try:
            self.cursor.execute("SELECT DISTINCT resolution_width FROM laptops ORDER BY resolution_width")
            widths = [row[0] for row in self.cursor.fetchall()]
            return widths
        except Exception as e:
            print("⚠️ Error fetching resolution_width:", e)
            return []

    def resolution_height(self):
        try:
            self.cursor.execute("SELECT DISTINCT resolution_height FROM laptops ORDER BY resolution_height")
            heights = [row[0] for row in self.cursor.fetchall()]
            return heights
        except Exception as e:
            print("⚠️ Error fetching resolution_height:", e)
            return []

    def touchscreen(self):
        try:
            self.cursor.execute("SELECT DISTINCT touchscreen FROM laptops ORDER BY touchscreen")
            touchscreen_vals = [row[0] for row in self.cursor.fetchall()]
            return touchscreen_vals
        except Exception as e:
            print("⚠️ Error fetching touchscreen:", e)
            return []

    def IPS_Panel(self):
        try:
            self.cursor.execute("SELECT DISTINCT IPS_Panel FROM laptops ORDER BY IPS_Panel")
            ips_vals = [row[0] for row in self.cursor.fetchall()]
            return ips_vals
        except Exception as e:
            print("⚠️ Error fetching IPS_Panel:", e)
            return []

    def Full_HD(self):
        try:
            self.cursor.execute("SELECT DISTINCT Full_HD FROM laptops ORDER BY Full_HD")
            full_hd_vals = [row[0] for row in self.cursor.fetchall()]
            return full_hd_vals
        except Exception as e:
            print("⚠️ Error fetching Full_HD:", e)
            return []

    def cpu_brand(self):
        try:
            self.cursor.execute("SELECT DISTINCT cpu_brand FROM laptops ORDER BY cpu_brand")
            brands = [row[0] for row in self.cursor.fetchall()]
            return brands
        except Exception as e:
            print("⚠️ Error fetching cpu_brand:", e)
            return []

    def cpu_speed(self):
        try:
            self.cursor.execute("SELECT DISTINCT cpu_speed FROM laptops ORDER BY cpu_speed")
            speeds = [row[0] for row in self.cursor.fetchall()]
            return speeds
        except Exception as e:
            print("⚠️ Error fetching cpu_speed:", e)
            return []

    def Ram(self):
        try:
            self.cursor.execute("SELECT DISTINCT Ram FROM laptops ORDER BY Ram")
            ram_vals = [row[0] for row in self.cursor.fetchall()]
            return ram_vals
        except Exception as e:
            print("⚠️ Error fetching Ram:", e)
            return []

    def Memory_Type(self):
        try:
            self.cursor.execute("SELECT DISTINCT Memory_Type FROM laptops ORDER BY Memory_Type")
            mem_types = [row[0] for row in self.cursor.fetchall()]
            return mem_types
        except Exception as e:
            print("⚠️ Error fetching Memory_Type:", e)
            return []

    def Primary_Memory(self):
        try:
            self.cursor.execute("SELECT DISTINCT Primary_Memory FROM laptops ORDER BY Primary_Memory")
            primary_mem = [row[0] for row in self.cursor.fetchall()]
            return primary_mem
        except Exception as e:
            print("⚠️ Error fetching Primary_Memory:", e)
            return []

    def Secondary_Memory(self):
        try:
            self.cursor.execute("SELECT DISTINCT Secondary_Memory FROM laptops ORDER BY Secondary_Memory")
            secondary_mem = [row[0] for row in self.cursor.fetchall()]
            return secondary_mem
        except Exception as e:
            print("⚠️ Error fetching Secondary_Memory:", e)
            return []

    def Gpu_brand(self):
        try:
            self.cursor.execute("SELECT DISTINCT Gpu_brand FROM laptops ORDER BY Gpu_brand")
            gpu_brands = [row[0] for row in self.cursor.fetchall()]
            return gpu_brands
        except Exception as e:
            print("⚠️ Error fetching Gpu_brand:", e)
            return []

    def OpSys(self):
        try:
            self.cursor.execute("SELECT DISTINCT OpSys FROM laptops ORDER BY OpSys")
            opsys_vals = [row[0] for row in self.cursor.fetchall()]
            return opsys_vals
        except Exception as e:
            print("⚠️ Error fetching OpSys:", e)
            return []

    def Weight(self):
        try:
            self.cursor.execute("SELECT DISTINCT Weight FROM laptops ORDER BY Weight")
            weights = [row[0] for row in self.cursor.fetchall()]
            return weights
        except Exception as e:
            print("⚠️ Error fetching Weight:", e)
            return []



    

        
if __name__ == "__main__":
    db = DB()
    db.migrate()
    db.new_table()
    db.OHE()


'''

st.code(code,language='python')