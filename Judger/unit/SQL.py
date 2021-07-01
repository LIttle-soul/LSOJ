import pymysql

class SQL:
    def __init__(self) -> None:
        self.db = pymysql.connect(
            host="182.92.71.47",
            user="root",
            port=3306,
            password="cjjdwws144",
            database="jol"
        )
        
    def read(self):
        with self.db.cursor() as cursor:
            sql = """SELECT
	                    solution.solution_id, 
	                    solution.problem_id, 
	                    solution.`language`, 
	                    source_code.source, 
	                    problem.time_limit, 
	                    problem.memory_limit, 
	                    problem.spj
                    FROM
	                    problem
	                INNER JOIN
	                    solution
	                ON 
		                problem.problem_id = solution.problem_id
	                INNER JOIN
	                    source_code
	                ON 
		                source_code.solution_id = solution.solution_id
                    WHERE
	                    solution.result < 2
                    ORDER BY
	                    solution.solution_id;"""
            cursor.execute(sql)
            data = cursor.fetchall()
        return data

    def update(self, time=0, memory=0, result=0, pass_rate=0, solution_id=0):
        with self.db.cursor() as cursor:
            sql = f"""
                    UPDATE
	                    solution
                    SET
	                    time={time},
	                    memory={memory},
	                    result={result},
	                    judgetime=NOW(),
	                    pass_rate={pass_rate:.02f}
                    WHERE
	                    solution_id={solution_id};"""
            cursor.execute(sql)
            self.db.commit()
        return True

    def insert(self, solution_id, error_info):
        with self.db.cursor() as cursor:
            sql = f"""
                    INSERT INTO
	                    compileinfo
		                (solution_id, error)
	                VALUES
		                ({solution_id}, '{error_info}');"""
            print(sql)
        return True

    def closed(self):
        self.db.close()

if __name__ == "__main__":
    sql = SQL()
    print(sql.read())
    sql.update(2500, 2025, 1, 0.9, 629433)
    sql.insert(629433, "你是傻逼")
    sql.closed()