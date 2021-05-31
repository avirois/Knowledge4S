from flask import Blueprint, render_template, request, session, redirect, current_app
import sqlite3

manage_types_blueprint = Blueprint("manage_types_blueprint", __name__, template_folder="templates")

@manage_types_blueprint.route('/manage_types')
def manage_types():
    
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')
    
    add = request.args.get("add")
    delete = request.args.get("delete")
    
    if(add != None):
        try:
            con = sqlite3.connect(current_app.config["DB_NAME"])
            cur = con.execute("INSERT INTO Types(Type) VALUES (?) ",(add,))
            con.commit()
        except Exception as e:
            print(e)
        finally:
            con.close()

        return redirect("/manage_types")

    elif(delete != None):
        try:
            con = sqlite3.connect(current_app.config["DB_NAME"])
            cur = con.execute("DELETE FROM Types WHERE ID = ?",(delete,))
            con.commit()
        except Exception as e:
            print(e)
        finally:
            con.close()

        return redirect("/manage_types")

    else:
        data = []
        try:
            con = sqlite3.connect(current_app.config["DB_NAME"])
            cur = con.execute("SELECT * FROM Types")
            for row in cur:
                data.append(row)
        except Exception as e:
            print(e)
        finally:
            con.close()

        return render_template("manageTypes.html",data = data)
