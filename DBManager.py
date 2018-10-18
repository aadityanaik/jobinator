import MySQLdb


class DBManager:
    db = None
    cursor = None

    def __init__(self):
        self.db = MySQLdb.connect(host="localhost",
                                  user="aaditya",
                                  passwd="arandompassword",
                                  db="JOB_PORTAL")

        self.cursor = self.db.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS POSTER("
                            "FNAME TEXT, "
                            "SNAME TEXT, "
                            "USERNAME VARCHAR(50) PRIMARY KEY, "
                            "ADDRESS TEXT, "
                            "COMPANY TEXT);")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS JOBS( "
                            "JOBID INT(10) PRIMARY KEY AUTO_INCREMENT, "
                            "JOBNAME TEXT, "
                            "DESCRIPTION TEXT,"
                            "POSTERID TEXT);")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS APPLICATIONS( "
                            "JOBID INT, "
                            "APPLICANTID VARCHAR(50), "
                            "FNAME TEXT, "
                            "SNAME TEXT, "
                            "ADDRESS TEXT, "
                            "RESUME BLOB, "
                            "PRIMARY KEY (JOBID, APPLICANTID));")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS APPLICANT("
                            "FNAME TEXT, "
                            "SNAME TEXT, "
                            "USERNAME VARCHAR(50) PRIMARY KEY, "
                            "ADDRESS TEXT, "
                            "RESUME BLOB);")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS USERPASS("
                            "USERNAME VARCHAR(50) PRIMARY KEY, "
                            "PASSWORD TEXT, "
                            "ACCOUNTTYPE BOOL);")  # TRUE means applicant, FALSE means poster

    def run(self, command, args=None):
        if command is not None:
            self.cursor.execute(command, args)
            self.db.commit()

            return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.db.close()
