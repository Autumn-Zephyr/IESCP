from flask import render_template, request, redirect, url_for
from flask import current_app as app 
import matplotlib.pyplot as plt
import datetime
from .models import *


def spon(id):
    sponsor = SPONSORS.query.filter_by(sponsor_id = id).first()
    return sponsor


@app.route("/edit_profile/sponsor/<int:sponsor_id>/", methods = ["POST"])
def edit_spon_profile(sponsor_id):

    sponsor = spon(sponsor_id)
    sponsor.company_name = request.form.get("name")
    sponsor.industry_type = request.form.get("industry")

    temp = (sponsor.company_name).strip().split(' ')
    search = ''
    for t in temp :
        search += t
    search += ' ' + sponsor.industry_type
    sponsor.search = search

    database.session.commit()
    return redirect(url_for("dashboard_spon_page", sponsor_id = sponsor_id))


@app.route("/delete/sponsor/<int:sponsor_id>/", methods = ["POST"])
def delete_spon(sponsor_id):
    sponsor = spon(sponsor_id)
    database.session.delete(sponsor)
    database.session.commit()
    return redirect(url_for("home"))


@app.route("/dashboard/sponsor/<int:sponsor_id>/")
def dashboard_spon_page(sponsor_id):

    sponsor = spon(sponsor_id)
    influencers = INFLUENCERS.query.all()
    advertisements = ADVERTISEMENTS.query.all()
    return render_template("users/spon-dashboard.html", sponsor = sponsor, influencers = influencers, campaigns = sponsor.campaign_details, advertisements = advertisements)


@app.route("/campaigns/sponsor/<int:sponsor_id>/") 
def campaigns_spon_page(sponsor_id):

    sponsor = spon(sponsor_id)
    return render_template("users/campaigns.html", campaigns = sponsor.campaign_details, sponsor = sponsor)


@app.route("/stats/sponsor/<int:sponsor_id>/") 
def stats_spon_page(sponsor_id):

    sponsor = spon(sponsor_id)

    active = CAMPAIGNS.query.filter_by(status = "Active", sponsor_id = sponsor_id).all()
    completed = CAMPAIGNS.query.filter_by(status = "Completed", sponsor_id = sponsor_id).all()
    campaigns = CAMPAIGNS.query.filter_by(sponsor_id = sponsor_id).all()
    accepted, pending, rejected, complete = [], [], [], []

    for camp in campaigns:
        accepted += ADVERTISEMENTS.query.filter_by(campaign_id = camp.campaign_id, acceptance = "Accepted").all()
        pending += ADVERTISEMENTS.query.filter_by(campaign_id = camp.campaign_id, sourse = "Sponsor", acceptance = "Pending").all()
        rejected += ADVERTISEMENTS.query.filter_by(campaign_id = camp.campaign_id, sourse = "Sponsor", acceptance = "Rejected").all()
        complete += ADVERTISEMENTS.query.filter_by(campaign_id = camp.campaign_id, acceptance = "Completed").all()

    path = "static/charts/sponsors/"

    labels = "Active", "Completed"
    counts = [len(active), len(completed)]
    fig, ax = plt.subplots()
    bar_colors = ['red', 'azure']
    ax.bar(labels, counts, color = bar_colors)
    ax.set_ylabel('No. of campaigns')
    fig.savefig(path + "campaigns.jpg")

    labels = "Accepted", "Pending", "Rejected", "Completed"
    counts = [len(accepted), len(pending), len(rejected), len(complete)]
    fig, ax = plt.subplots()
    bar_colors = ["orange", "orange", "orange", "orange"]
    ax.bar(labels, counts, color = bar_colors)
    ax.set_ylabel('No. of advertisements')
    fig.savefig(path + "advertisements.jpg")


    return render_template("users/spon-stats.html", sponsor = sponsor, campaigns = sponsor.campaign_details)


@app.route("/find/sponsor/<int:sponsor_id>/") 
def find_spon_page(sponsor_id):

    sponsor = spon(sponsor_id)
    campaigns = CAMPAIGNS.query.filter_by(sponsor_id = sponsor_id)
    influencers = INFLUENCERS.query.filter_by(flagged = False)
    return render_template("users/spon-find.html", sponsor = sponsor, campaigns = campaigns, influencers = influencers)


@app.route("/campaign/add/<int:sponsor_id>/", methods = ["POST"])
def new_campaign(sponsor_id):

    sponsor = spon(sponsor_id)

    name = request.form.get("name")
    description = request.form.get("description")
    start = datetime.date.today()
    end = datetime.datetime.strptime(request.form.get("end"), '%Y-%m-%d').date()
    visib = request.form.get("visibility")
    ads = request.form.get("ads")
    budget = request.form.get("budget")

    temp = name.strip().split(' ')
    search = ''
    for t in temp :
        search += t
    search += ' ' + sponsor.search

    campaign = CAMPAIGNS(campaign_name = name, campaign_description = description, visibility = visib, start_date = start, end_date = end, budget = budget, no_of_ads = ads, ads_completed = 0, campaign_type = sponsor.industry_type, sponsor_id = sponsor.sponsor_id, status = "Active", search = search)
    database.session.add(campaign)
    database.session.commit()

    return redirect(url_for("campaigns_spon_page", sponsor_id = sponsor.sponsor_id))
    

@app.route("/campaign/edit/<int:sponsor_id>/", methods = ["POST"])
def edit_campaign(sponsor_id):

    name = request.form.get("name")
    description = request.form.get("description")
    end = datetime.datetime.strptime(request.form.get("end"), '%Y-%m-%d').date()
    visib = request.form.get("visibility")
    ads = request.form.get("ads")
    bud = request.form.get("budget")

    campaign = CAMPAIGNS.query.filter_by(sponsor_id = sponsor_id, campaign_name = name).first()
    campaign.campaign_description = description
    campaign.end_date = end
    campaign.visibility = visib
    campaign.no_of_ads = ads
    campaign.budget = bud
    database.session.commit()

    return redirect(url_for("campaigns_spon_page", sponsor_id = sponsor_id))


@app.route("/campaign/delete/<int:sponsor_id>/", methods = ["POST"])
def delete_campaign(sponsor_id):

    name = request.form.get("name")
    campaign = CAMPAIGNS.query.filter_by(sponsor_id = sponsor_id, campaign_name = name).first()
    database.session.delete(campaign)
    database.session.commit()
    
    return redirect(url_for("campaigns_spon_page", sponsor_id = sponsor_id))


@app.route("/request_ad/sponsor/<int:sponsor_id>/", methods = ["POST"])
def request_inf_ad(sponsor_id):

    inf_id = request.form.get("id")
    camp_id = request.form.get("camp_id")
    req = request.form.get("requirements")
    amount = request.form.get("amount")

    new_req = ADVERTISEMENTS(influencer_id = inf_id, campaign_id = camp_id, requirements = req, amount = amount, sourse = "Sponsor", acceptance = "Pending", work_confirmation = False, payment_confirmation = False, rating = 0)
    database.session.add(new_req)
    database.session.commit()

    return redirect(url_for("find_spon_page", sponsor_id = sponsor_id))


@app.route("/accept_ad/sponsor/<int:advertisement_id>/") 
def accept_ad_spon(advertisement_id):

    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    advertisement.acceptance = "Accepted"
    advertisement.sourse = "Sponsor"
    campaign = CAMPAIGNS.query.filter_by(campaign_id = advertisement.campaign_id).first()
    database.session.commit()

    return redirect(url_for("dashboard_spon_page", sponsor_id = campaign.sponsor_id))


@app.route("/reject_ad/advertisement/<int:advertisement_id>/") 
def reject_ad_spon(advertisement_id):

    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    advertisement.acceptance = "Rejected"
    campaign = CAMPAIGNS.query.filter_by(campaign_id = advertisement.campaign_id).first()
    database.session.commit()

    return redirect(url_for("dashboard_spon_page", sponsor_id = campaign.sponsor_id))


@app.route("/negotiate_ad/sponsor/<int:sponsor_id>/", methods = ["POST"]) 
def negotiate_ad_spon(sponsor_id):

    advertisement_id = request.form.get("ad_id")
    amount = request.form.get("amount")
    requirements = request.form.get("requirements")

    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    advertisement.amount = amount
    advertisement.sourse = "Sponsor"
    advertisement.requirements = requirements
    database.session.commit()

    return redirect(url_for("dashboard_spon_page", sponsor_id = sponsor_id))


@app.route("/payment_ad/sponsor/<int:sponsor_id>/", methods = ["POST"]) 
def payment_confirm_ad_spon(sponsor_id):

    advertisement_id = request.form.get("ad_id")
    amount = request.form.get("amount")
    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    advertisement.acceptance = "Completed"
    advertisement.payment_confirmation = True
    advertisement.rating = int(request.form.get("rating"))

    influencer = INFLUENCERS.query.filter_by(influencer_id = advertisement.influencer_id).first()
    influencer.earning += int(amount)
    influencer.rating = ((influencer.rating * influencer.ads_done) + advertisement.rating)/(influencer.ads_done + 1)
    influencer.ads_done += 1

    campaign = CAMPAIGNS.query.filter_by(campaign_id = advertisement.campaign_id).first()
    campaign.ads_completed += 1
    if campaign.no_of_ads == campaign.ads_completed:
        campaign.status = "Completed"

    database.session.commit()
    return redirect(url_for("dashboard_spon_page", sponsor_id = sponsor_id))


@app.route("/delete_ad/sponsor/<int:advertisement_id>/")
def delete_ad_spon(advertisement_id):

    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    campaign = CAMPAIGNS.query.filter_by(campaign_id = advertisement.campaign_id).first()
    sponsor_id = campaign.sponsor_id
    database.session.delete(advertisement)
    database.session.commit()
    
    return redirect(url_for("campaigns_spon_page", sponsor_id = sponsor_id))


@app.route("/edit_ad/sponsor/<int:sponsor_id>/", methods = ["POST"])
def edit_ad_apon(sponsor_id):

    advertisement_id = request.form.get("id")
    req = request.form.get("requirements")
    amount = request.form.get("amount")

    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    advertisement.requirements = req
    advertisement.amount = amount
    database.session.commit()
    
    return redirect(url_for("campaigns_spon_page", sponsor_id = sponsor_id))


@app.route("/search/sponsor/<int:sponsor_id>/")
def search_spon(sponsor_id):

    word = "%" + request.args.get("word") + "%"
    campaigns = CAMPAIGNS.query.filter(CAMPAIGNS.search.like(word), CAMPAIGNS.sponsor_id == sponsor_id).all()
    influencers = INFLUENCERS.query.filter(INFLUENCERS.search.like(word), INFLUENCERS.flagged == 0).all()
    sponsor = spon(sponsor_id)
    return render_template("users/spon-find.html", campaigns = campaigns, sponsor = sponsor, influencers = influencers)


# code ends

