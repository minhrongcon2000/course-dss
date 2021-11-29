import re

with open("dummy.txt", "r") as f, open("process_statement.txt", "w") as sql_f:
    statements = []
    for line in f:
        statement = "INSERT INTO Course VALUES"
        sql_statement = line.strip()
        m = re.search("[^INSERT INTO Course VALUES]", sql_statement)
        main_part = sql_statement[m.span()[0]:-1].split(",")
        main_part.pop()
        main_part[-1] += ")"
        
        final_statement = statement + ",".join(main_part)
        sql_f.write(final_statement + ";\n")
