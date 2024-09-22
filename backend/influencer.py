from flask import render_template, request, redirect, url_for
from flask import current_app as app 
import matplotlib.pyplot as plt
from .models import *


def inf(id):
    influencer = INFLUENCERS.query.filter_by(influencer_id = id).first()
    return influencer


@app.route("/edit_profile/influencer/<int:influencer_id>/", methods = ["POST"])
def edit_inf_profile(influencer_id):

    influencer = inf(influencer_id)
    influencer.first_name = request.form.get("fname")
    influencer.last_name = request.form.get("lname")
    influencer.niche = request.form.get("niche")
    influencer.reach = request.form.get("reach")
    platforms = request.form.getlist("platforms")
    influencer.platforms = ""
    for plat in platforms:
        influencer.platforms += plat + " "
    
    influencer.search = influencer.first_name + influencer.last_name + ' ' + influencer.niche + ' ' + influencer.reach + ' ' + influencer.platforms
    
    database.session.commit()
    return redirect(url_for("dashboard_inf_page", influencer_id = influencer_id))


@app.route("/delete/influencer/<int:influencer_id>/", methods = ["POST"])
def delete_inf(influencer_id):

    influencer = inf(influencer_id)
    database.session.delete(influencer)
    database.session.commit()
    return redirect(url_for("home"))


@app.route("/dashboard/influencer/<int:influencer_id>/")
def dashboard_inf_page(influencer_id):

    influencer = inf(influencer_id)
    advertisements = ADVERTISEMENTS.query.filter_by(influencer_id = influencer.influencer_id)
    campaigns = CAMPAIGNS.query.all()
    sponsors = SPONSORS.query.all()
    return render_template("users/inf-dashboard.html", influencer = influencer, advertisements = advertisements, sponsors = sponsors, campaigns = campaigns)


@app.route("/stats/influencer/<int:influencer_id>/") 
def stats_inf_page(influencer_id):

    influencer = inf(influencer_id)

    accepted, pending, rejected, complete = [], [], [], []

    accepted += ADVERTISEMENTS.query.filter_by(influencer_id = influencer_id,  acceptance = "Accepted").all()
    pending += ADVERTISEMENTS.query.filter_by(influencer_id = influencer_id, sourse = "Influencer", acceptance = "Pending").all()
    rejected += ADVERTISEMENTS.query.filter_by(influencer_id = influencer_id, sourse = "Influencer", acceptance = "Rejected").all()
    complete += ADVERTISEMENTS.query.filter_by(influencer_id = influencer_id, acceptance = "Completed").all()

    path = "static/charts/influencers/"
    
    labels = "Accepted", "Pending", "Rejected", "Completed"
    counts = [len(accepted), len(pending), len(rejected), len(complete)]
    fig, ax = plt.subplots()
    bar_colors = ["orange", "orange", "orange", "orange"]
    ax.bar(labels, counts, color = bar_colors)
    ax.set_ylabel('No. of advertisements')
    fig.savefig(path + "advertisements.jpg")

    return render_template("users/inf-stats.html", influencer = influencer, advertisements = influencer.advertisement_details)


@app.route("/find/influencer/<int:influencer_id>/") 
def find_inf_page(influencer_id):

    influencer = inf(influencer_id)
    sponsors = SPONSORS.query.all()
    campaigns = CAMPAIGNS.query.filter_by(flagged = False, status = "Active")
    return render_template("users/inf-find.html", influencer = influencer, campaigns = campaigns, sponsors = sponsors)


@app.route("/request_ad/influencer/<int:influencer_id>/", methods = ["POST"])
def request_spon_ad(influencer_id):

    camp_id = request.form.get("camp_id")
    req = request.form.get("requirements")
    amount = request.form.get("amount")

    new_req = ADVERTISEMENTS(influencer_id = influencer_id, campaign_id = camp_id, requirements = req, amount = amount, sourse = "Influencer", acceptance = "Pending", work_confirmation = False, payment_confirmation = False, rating = 0)
    database.session.add(new_req)
    database.session.commit()

    return redirect(url_for("find_inf_page", influencer_id = influencer_id))


@app.route("/accept_ad/influencer/<int:advertisement_id>/") 
def accept_ad_inf(advertisement_id):

    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    advertisement.acceptance = "Accepted"
    database.session.commit()

    return redirect(url_for("dashboard_inf_page", influencer_id = advertisement.influencer_id))


@app.route("/reject_ad/influencer/<int:advertisement_id>/") 
def reject_ad_inf(advertisement_id):

    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    advertisement.acceptance = "Rejected"
    database.session.commit()

    return redirect(url_for("dashboard_inf_page", influencer_id = advertisement.influencer_id))


@app.route("/negotiate_ad/influencer/<int:influencer_id>/", methods = ["POST"]) 
def negotiate_ad_inf(influencer_id):

    advertisement_id = request.form.get("ad_id")
    amount = request.form.get("amount")

    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    advertisement.amount = amount
    advertisement.sourse = "Influencer"
    database.session.commit()

    return redirect(url_for("dashboard_inf_page", influencer_id = influencer_id))


@app.route("/work_confirm/influencer/<int:advertisement_id>/") 
def work_confirm_ad_inf(advertisement_id):

    advertisement = ADVERTISEMENTS.query.filter_by(advertisement_id = advertisement_id).first()
    advertisement.work_confirmation = True
    database.session.commit()

    return redirect(url_for("dashboard_inf_page", influencer_id = advertisement.influencer_id))


@app.route("/search/influencer/<int:influencer_id>/")
def search_inf(influencer_id):

    word = "%" + request.args.get("word") + "%"
    campaigns = CAMPAIGNS.query.filter(CAMPAIGNS.campaign_name.like(word), CAMPAIGNS.flagged == 0).all() + CAMPAIGNS.query.filter(CAMPAIGNS.campaign_type.like(word), CAMPAIGNS.flagged == 0).all()
    sponsors = SPONSORS.query.all()
    influencer = inf(influencer_id)
    return render_template("users/inf-find.html", campaigns = campaigns, influencer = influencer, sponsors = sponsors)


# code ends
