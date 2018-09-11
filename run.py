import os
from ems import app, database_name, db

if __name__ == "__main__":
    exist = os.path.isfile('ems/'+database_name)
    if not exist:
        db.create_all()
        
    app.run(debug=True, use_reloader=True)
