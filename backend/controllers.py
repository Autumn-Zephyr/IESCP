from flask import render_template, request
from flask import current_app as app            # Alias for current running app
from .models import *



@app.route("/", methods = ["GET", "POST"])      # login URL
def home():

    if request.method == "POST":

        author = request.form.get("AUTHOR")
        uname = request.form.get("USERNAME")
        pword = request.form.get("PASSWORD")

        details = LOGIN.query.filter_by(user_name = uname, password = pword, role = author).first()
            
        if details:
            if author == "Admin":
                # campaigns = fetch_campaigns()
                # return render_template("admins/dashboard.html", username = uname, campaigns = campaigns)
                return redirect(url_for("dashboard_admin_page", username = uname))
            
            elif author == "Influencer":
                influencer = INFLUENCERS.query.filter_by(user_name = uname).first()
                return redirect(url_for("dashboard_inf_page", influencer_id = influencer.influencer_id))

            elif author == "Sponsor":
                sponsor = SPONSORS.query.filter_by(user_name = uname).first()
                return redirect(url_for("dashboard_spon_page", sponsor_id = sponsor.sponsor_id))

            return render_template("homepage.html", invalid = "CHOOSE A CORRECT AUTHOR TYPE.")
        
        return render_template("homepage.html", invalid = "EITHER AUTHOR TYPE USERNAME OR PASSWORD IS WRONG.")

    return render_template("homepage.html")



@app.route("/inf-register/", methods = ["GET", "POST"])      # registration URL for influencer
def inf_register():

    if request.method == "POST":

        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        uname = request.form.get("username")
        pword = request.form.get("password")
        cpword = request.form.get("conf-password")
        reach = request.form.get("reach")
        niche = request.form.get("niche")
        platforms = request.form.getlist("platforms")
        plat_info = ""

        if pword != cpword:
            return render_template("inf-register.html", invalid = "PASSWORD CONFIRMATION NOT SATISFIED. RE-ENTER PASSWORD.")

        details = LOGIN.query.filter_by(user_name = uname).first() 
        if not details:
            for plat in platforms:
                plat_info += plat + " "
                  
            search = fname + lname + ' ' + niche + ' ' + reach + ' ' + plat_info

            new_login = LOGIN(user_name = uname, password = pword, role = "Influencer")
            new_user = INFLUENCERS(user_name = uname, first_name = fname, last_name = lname, niche = niche, reach = reach, platforms = plat_info, earning = 0, rating = 0, ads_done = 0, flagged = False, search = search)

            database.session.add(new_user)
            database.session.add(new_login)
            database.session.commit()
            return render_template("homepage.html", invalid = "LOG IN TO ACCESS.")
        
        return render_template("inf-register.html", invalid = "SORRY, USERNAME IS TAKEN!!")
    
    return render_template("inf-register.html")



@app.route("/spon-register/", methods = ["GET", "POST"])     # registration URL for sponsor
def spon_register():
    
    if request.method == "POST":

        name = request.form.get("name")
        uname = request.form.get("username")
        pword = request.form.get("password")
        cpword = request.form.get("conf-password")
        industry = request.form.get("INDUSTRY")

        temp = name.strip().split(' ')
        search = ''
        for t in temp :
            search += t
        search += ' ' + industry

        if pword != cpword:
            return render_template("spon-register.html", invalid = "PASSWORD CONFIRMATION NOT SATISFIED. RE-ENTER PASSWORD.")

        details = LOGIN.query.filter_by(user_name = uname).first() 
        if not details:
            new_login = LOGIN(user_name = uname, password = pword, role = "Sponsor")
            new_user = SPONSORS(user_name = uname, company_name = name, industry_type = industry, flagged = False, search = search)

            database.session.add(new_user)
            database.session.add(new_login)
            database.session.commit()
            return render_template("homepage.html", invalid = "LOG IN TO ACCESS.")
        
        return render_template("spon-register.html", invalid = "SORRY, USERNAME IS TAKEN!!")
    
    return render_template("spon-register.html")



from .admin import *        # importing admin.py from backend
from .sponsor import *      # importing spoonsor.py frpm backend
from .influencer import *   # importing influencer.py from backend


# code ends
