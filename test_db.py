from scripts.database_op.db_op import *
from scripts.utils.log_to_file import *

open_log_file()

connect_to_db()
#insert_to_db("RECO_ID_1425", "juniperhollow", "/srt2/2424rwe/sfsfsdf")
print(select_from_db("RECO_ID_1425"))
close_log_file()