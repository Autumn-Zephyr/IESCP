from flask_restful import Api, Resource, reqparse
from datetime import datetime
from .models import *

api = Api()


sponsor_parser = reqparse.RequestParser()
sponsor_parser.add_argument("user_name")
sponsor_parser.add_argument("company_name")
sponsor_parser.add_argument("industry_type")
sponsor_parser.add_argument("password")
sponsor_parser.add_argument("conf_password")


influencer_parser = reqparse.RequestParser()
influencer_parser.add_argument("user_name")
influencer_parser.add_argument("first_name")
influencer_parser.add_argument("last_name")
influencer_parser.add_argument("niche")
influencer_parser.add_argument("platforms")
influencer_parser.add_argument("reach")
influencer_parser.add_argument("password")
influencer_parser.add_argument("conf_password")


campaign_parser = reqparse.RequestParser()
campaign_parser.add_argument("campaign_name")
campaign_parser.add_argument("campaign_description")
campaign_parser.add_argument("start_date")
campaign_parser.add_argument("end_date")
campaign_parser.add_argument("visibility")
campaign_parser.add_argument("no_of_ads")
campaign_parser.add_argument("budget")




class Sponsor_API(Resource):

    def get(self, sponsor_id):
        sponsor = SPONSORS.query.filter_by(sponsor_id = sponsor_id).first()
        spon_details = {}
        spon_details["sponsor_id"] = sponsor.sponsor_id
        spon_details["user_name"] = sponsor.user_name
        spon_details["company_name"] = sponsor.company_name
        spon_details["industry_type"] = sponsor.industry_type
        spon_details["flagged"] = sponsor.flagged

        return spon_details
    

    def post(self):

        sponsor_data = sponsor_parser.parse_args()

        if sponsor_data["password"] != sponsor_data["conf_password"]:
            return "Password Confirmation not satisfied! Re-enter.", 401

        details = LOGIN.query.filter_by(user_name = sponsor_data["user_name"]).first() 
        if details:
            return "Username is taken! Choose a different username.", 401

        temp = sponsor_data["company_name"].strip().split(' ')
        search = ''
        for t in temp :
            search += t
        search += ' ' + sponsor_data["industry_type"]

        new_sponsor = SPONSORS(user_name = sponsor_data["user_name"], company_name = sponsor_data["company_name"], industry_type = sponsor_data["industry_type"], flagged = False, search = search)
        database.session.add(new_sponsor)

        new_login = LOGIN(user_name = sponsor_data["user_name"], password = sponsor_data["password"], role = "Sponsor")
        database.session.add(new_login)

        database.session.commit()
        return "Sponsor Created!", 201
    
    
    def put(self, sponsor_id):

        sponsor_data = sponsor_parser.parse_args()
        sponsor = SPONSORS.query.filter_by(sponsor_id = sponsor_id).first()

        if sponsor:
            sponsor.company_name = sponsor_data["company_name"]
            sponsor.industry_type = sponsor_data["industry_type"]

            temp = sponsor_data["company_name"].strip().split(' ')
            search = ''
            for t in temp :
                search += t
            search += ' ' + sponsor_data["industry_type"]
            sponsor.search = search

            database.session.commit()
            return "Sponsor Updated!", 201
        return "Sponsor Not Found!", 404
    

    def delete(self, sponsor_id):
        sponsor = SPONSORS.query.filter_by(sponsor_id = sponsor_id).first()
        if sponsor:
            login = LOGIN.query.filter_by(user_name = sponsor.user_name).first()
            database.session.delete(sponsor)
            database.session.delete(login)
            database.session.commit()
            return "Sponsor Deleted!", 201
        return "Sponsor Not Found!", 404


api.add_resource(Sponsor_API, "/api/get/sponsor/<int:sponsor_id>", "/api/post/sponsor", "/api/put/sponsor/<int:sponsor_id>", "/api/delete/sponsor/<int:sponsor_id>")



class Influencer_API(Resource):

    def get(self, influencer_id):
        influencer = SPONSORS.query.filter_by(influencer_id = influencer_id).first()
        spon_details = {}
        spon_details["influencer_id"] = influencer.influencer_id
        spon_details["user_name"] = influencer.user_name
        spon_details["first_name"] = influencer.first_name
        spon_details["last_name"] = influencer.last_name
        spon_details["niche"] = influencer.niche
        spon_details["reach"] = influencer.reach
        spon_details["platforms"] = influencer.platforms
        spon_details["flagged"] = influencer.flagged

        return spon_details
    

    def post(self):

        influencer_data = influencer_parser.parse_args()

        if influencer_data["password"] != influencer_data["conf_password"]:
            return "Password Confirmation not satisfied! Re-enter.", 401

        details = LOGIN.query.filter_by(user_name = influencer_data["user_name"]).first() 
        if details:
            return "Username is taken! Choose a different username.", 401

        search = influencer_data["first_name"] + influencer_data["last_name"] + ' ' + influencer_data["niche"] + ' ' + influencer_data["reach"] + ' ' + influencer_data["platforms"]

        new_influencer = INFLUENCERS(user_name = influencer_data["user_name"],first_name = influencer_data["first_name"], last_name = influencer_data["last_name"], niche = influencer_data["niche"], platforms = influencer_data["platforms"], reach = influencer_data["reach"], ads_done = 0, earning = 0, rating = 0, flagged = False, search = search)
        database.session.add(new_influencer)

        new_login = LOGIN(user_name = influencer_data["user_name"], password = influencer_data["password"], role = "Influencer")
        database.session.add(new_login)

        database.session.commit()
        return "Influencer Created!", 201
    
    
    def put(self, influencer_id):

        influencer_data = influencer_parser.parse_args()
        influencer = INFLUENCERS.query.filter_by(influencer_id = influencer_id).first()

        if influencer:
            influencer.first_name = influencer_data["first_name"]
            influencer.last_name = influencer_data["last_name"]
            influencer.niche = influencer_data["niche"]
            influencer.reach = influencer_data["reach"]
            influencer.platforms = influencer_data["platforms"]

            search = influencer_data["first_name"] + influencer_data["last_name"] + ' ' + influencer_data["niche"] + ' ' + influencer_data["reach"] + ' ' + influencer_data["platforms"]
            influencer.search = search 
            
            database.session.commit()
            return "Influencer Updated!", 201
        return "Influencer Not Found!", 404
    

    def delete(self, influencer_id):
        influencer = INFLUENCERS.query.filter_by(influencer_id = influencer_id).first()
        if influencer:
            login = LOGIN.query.filter_by(user_name = influencer.user_name).first()
            database.session.delete(influencer)
            database.session.delete(login)
            database.session.commit()
            return "Influencer Deleted!", 201
        return "Influencer Not Found!", 404


api.add_resource(Influencer_API, "/api/get/influencer/<int:influencer_id>", "/api/post/influencer", "/api/put/influencer/<int:influencer_id>", "/api/delete/influencer/<int:influencer_id>")



class Campaign_API(Resource):

    def get(self, sponsor_id):

        campaigns = CAMPAIGNS.query.filter_by(sponsor_id = sponsor_id).all()
        sponsor_campaign = []
        for campaign in campaigns:
            campaign_details = {}
            campaign_details["campaign_id"] = campaign.campaign_id
            campaign_details["campaign_name"] = campaign.campaign_name
            campaign_details["campaign_description"] = campaign.campaign_description
            campaign_details["start_date"] = campaign.start_date.strftime('%Y-%m-%d')
            campaign_details["end_date"] = campaign.end_date.strftime('%Y-%m-%d')
            campaign_details["visibility"] = campaign.visibility
            campaign_details["no_of_ads"] = campaign.no_of_ads
            campaign_details["ads_completed"] = campaign.no_of_ads
            campaign_details["budget"] = campaign.budget
            campaign_details["campaign_type"] = campaign.campaign_type
            sponsor_campaign.append(campaign_details)
        
        return sponsor_campaign


    def post(self, sponsor_id):

        campaign_data = campaign_parser.parse_args()
        sponsor = SPONSORS.query.filter_by(sponsor_id = sponsor_id).first()

        temp = campaign_data["campaign_name"].strip().split(' ')
        search = ''
        for t in temp :
            search += t
        search += ' ' + sponsor.search

        start_date = datetime.strptime(campaign_data["start_date"], '%Y-%m-%d').date()
        end_date = datetime.strptime(campaign_data["end_date"], '%Y-%m-%d').date()

        new_campaign = CAMPAIGNS(campaign_name = campaign_data["campaign_name"], campaign_description = campaign_data["campaign_description"], sponsor_id = sponsor_id, visibility = campaign_data["visibility"], no_of_ads = campaign_data["no_of_ads"], ads_completed = 0, budget = campaign_data["budget"], start_date = start_date, end_date = end_date, flagged = False, campaign_type = sponsor.industry_type, search = search, status = "Active")
        database.session.add(new_campaign)
        database.session.commit()

        return "Campaign Created!", 201
    
    
    def put(self, campaign_id):

        campaign_data = campaign_parser.parse_args()
        campaign = CAMPAIGNS.query.filter_by(campaign_id = campaign_id)

        if campaign:
            campaign.campaign_description = campaign_data["campaign_description"]
            campaign.end_date = campaign_data["end_date"]
            campaign.visibility = campaign_data["visibility"]
            campaign.no_of_ads = campaign_data["no_of_ads"]
            campaign.budget = campaign_data["budget"]
            return "Campaign Updated!", 201
        return "Campaign Not Found!", 404


    def delete(self, campaign_id):
        campaign = CAMPAIGNS.query.filter_by(campaign_id = campaign_id)
        if campaign:
            database.session.delete(campaign)
            database.session.commit()
            return "Campaign Deleted!", 201
        return "Campaign Not Found!", 404


api.add_resource(Campaign_API, "/api/get/campaigns/<int:sponsor_id>", "/api/post/campaigns/<int:sponsor_id>", "/api/put/campaigns/<int:campaign_id>", "/api/delete/campaigns/<int:campaign_id>")
