from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy() # instance of SQLAlchemy

class LOGIN(database.Model):
    __tablename__ = "login_details"
    user_name = database.Column(database.String, primary_key = True)
    password = database.Column(database.String, nullable = False)
    role = database.Column(database.String, nullable = False, default = "Admin")


class INFLUENCERS(database.Model):
    __tablename__ = "influencer_details"
    influencer_id = database.Column(database.Integer, autoincrement = True, primary_key = True)
    user_name = database.Column(database.String, unique = True, nullable = False)
    first_name = database.Column(database.String, nullable = False)
    last_name = database.Column(database.String, nullable = True)
    niche = database.Column(database.String, nullable = False)
    platforms = database.Column(database.String, nullable = False)
    rating = database.Column(database.Integer, nullable = False, default = 0)
    earning = database.Column(database.Integer, nullable = False, default = 0)
    reach = database.Column(database.Integer, nullable = False)
    ads_done = database.Column(database.Integer, nullable = False, default = 0)
    flagged = database.Column(database.Boolean, nullable = False, default = False)
    search = database.Column(database.String, nullable = False)
    advertisement_details = database.relationship("ADVERTISEMENTS", cascade = "all, delete", backref = "influencer_details")


class SPONSORS(database.Model):
    __tablename__ = "sponsor_details"
    sponsor_id = database.Column(database.Integer, autoincrement = True, primary_key = True)
    user_name = database.Column(database.String, unique = True, nullable = False)
    company_name = database.Column(database.String, nullable = False)
    industry_type = database.Column(database.String, nullable = False)
    flagged = database.Column(database.Boolean, nullable = False, default = False)
    search = database.Column(database.String, nullable = False)
    campaign_details = database.relationship("CAMPAIGNS", cascade = "all, delete", backref = "sponsor_details")
    

class CAMPAIGNS(database.Model):
    __tablename__ = "campaign_details"
    campaign_id = database.Column(database.Integer, primary_key = True, autoincrement = True)
    campaign_name = database.Column(database.String, nullable = False)
    sponsor_id = database.Column(database.Integer, database.ForeignKey("sponsor_details.sponsor_id"), nullable = False)
    start_date = database.Column(database.Date, nullable = False)
    end_date = database.Column(database.Date, nullable = False)
    budget = database.Column(database.Integer, nullable = False)
    campaign_description = database.Column(database.String, nullable = False)
    no_of_ads = database.Column(database.Integer, nullable = False)
    ads_completed = database.Column(database.Integer, nullable = False, default = 0)
    visibility = database.Column(database.String, nullable = False)
    campaign_type = database.Column(database.String, nullable = False)
    status = database.Column(database.String, nullable = False)
    flagged = database.Column(database.Boolean, nullable = False, default = False)
    search = database.Column(database.String, nullable = False)
    advertisement_details = database.relationship("ADVERTISEMENTS", cascade = "all, delete", backref = "campaign_details")


class ADVERTISEMENTS(database.Model):
    __tablename__ = "advertisement_details"
    advertisement_id = database.Column(database.Integer, primary_key = True, autoincrement = True)
    campaign_id = database.Column(database.Integer, database.ForeignKey("campaign_details.campaign_id"), nullable = False)
    influencer_id = database.Column(database.Integer, database.ForeignKey("influencer_details.influencer_id"), nullable = False)
    sourse = database.Column(database.String, nullable = False)
    amount = database.Column(database.Integer, nullable = False)
    requirements = database.Column(database.String, nullable = False)
    acceptance = database.Column(database.String, nullable = False, default = "Pending")
    work_confirmation = database.Column(database.Boolean, nullable = False)
    payment_confirmation = database.Column(database.Boolean, nullable = False)
    rating = database.Column(database.Integer, nullable = False, default = 0)


# code ends