from flask import render_template, request, redirect, url_for
from flask import current_app as app 
import matplotlib.pyplot as plt
import numpy as np
from .models import *




@app.route("/dashboard/admin/<string:username>/")
def dashboard_admin_page(username):

    campaigns = CAMPAIGNS.query.all()
    influencers = INFLUENCERS.query.all()
    advertisements = ADVERTISEMENTS.query.all()
    sponsors = SPONSORS.query.all()

    return render_template("admins/dashboard.html", username = username, sponsors = sponsors, influencers = influencers, campaigns = campaigns, advertisements = advertisements)


@app.route("/find/admin/<string:username>/") 
def find_admin_page(username):
    
    campaigns = CAMPAIGNS.query.all()
    influencers = INFLUENCERS.query.all()
    sponsors = SPONSORS.query.all()
    spons = SPONSORS.query.all()

    return render_template("admins/find.html", username = username, sponsors = sponsors, influencers = influencers, campaigns = campaigns, spons = spons)


@app.route("/stats/admin/<string:username>/") 
def stats_admin_page(username):
    
    campaigns = CAMPAIGNS.query.all()
    active = CAMPAIGNS.query.filter_by(status = "Active").all()
    completed = CAMPAIGNS.query.filter_by(status = "Completed").all()
    f_camp = CAMPAIGNS.query.filter_by(flagged = True).all()
    uf_camp = CAMPAIGNS.query.filter_by(flagged = False).all()

    influencers = INFLUENCERS.query.all()
    sponsors = SPONSORS.query.all()
    f_inf = INFLUENCERS.query.filter_by(flagged = True).all()
    uf_inf = INFLUENCERS.query.filter_by(flagged = False).all()
    f_spon = SPONSORS.query.filter_by(flagged = True).all()
    uf_spon = SPONSORS.query.filter_by(flagged = False).all()

    path = "static/charts/admins/"

    labels = "Sponsors", "Influencers"
    sizes = [len(sponsors), len(influencers)]
    colors=["plum", "xkcd:pink"]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels = labels, autopct = '%1.1f%%', colors = colors)
    fig.savefig(path + "users.jpg")

    labels = "Influencers", "Sponsors"
    counts = {"Flagged": np.array([len(f_inf), len(f_spon)]), "Unflagged": np.array([len(uf_inf), len(uf_spon)])}
    fig, ax = plt.subplots()
    bottom = np.zeros(2)
    bar_colors = ['blue', 'orange']
    for f, val in counts.items():
        p = ax.bar(labels, val, label = f, bottom = bottom)
        bottom += val
        ax.bar_label(p, label_type='center')
    ax.set_ylabel('No. of flagged and unflagged users')
    ax.legend()
    fig.savefig(path + "users_flagged.jpg")

    labels = "Active", "Completed"
    counts = [len(active), len(completed)]
    fig, ax = plt.subplots()
    bar_colors = ['red', 'azure']
    ax.bar(labels, counts, color = bar_colors)
    ax.set_ylabel('No. of campaigns')
    fig.savefig(path + "campaigns.jpg")

    labels = "Flagged", "Unflagged"
    counts = [len(f_camp), len(uf_camp)]
    colors=["cyan", "cyan"]
    fig, ax = plt.subplots()
    ax.bar(labels, counts, color = colors)
    ax.set_ylabel('No. of advertisements')
    fig.savefig(path + "camps_flagged.jpg")

    return render_template("admins/stats.html", username = username, sponsors = sponsors, influencers = influencers, campaigns = campaigns)


@app.route("/unflag/admin/<string:username>/<string:user_name>/") 
def unflag_user_admin_page(username, user_name):

    user = LOGIN.query.filter_by(user_name = user_name).first()
    if user.role == "Sponsor":
        U = SPONSORS.query.filter_by(user_name = user_name).first()
    elif user.role == "Influencer":
        U = INFLUENCERS.query.filter_by(user_name = user_name).first()

    U.flagged = False
    database.session.commit()
    return redirect(url_for("dashboard_admin_page", username = username))


@app.route("/unflag/admin/<string:username>/<int:campaign_id>/") 
def unflag_camp_admin_page(username, campaign_id):

    campaign = CAMPAIGNS.query.filter_by(campaign_id = campaign_id).first()
    campaign.flagged = False
    database.session.commit()
    return redirect(url_for("dashboard_admin_page", username = username))
        

@app.route("/flag/admin/<string:username>/<string:user_name>/") 
def flag_user_admin_page(username, user_name):

    user = LOGIN.query.filter_by(user_name = user_name).first()
    if user.role == "Sponsor":
        U = SPONSORS.query.filter_by(user_name = user_name).first()
    elif user.role == "Influencer":
        U = INFLUENCERS.query.filter_by(user_name = user_name).first()

    U.flagged = True
    database.session.commit()
    return redirect(url_for("find_admin_page", username = username))


@app.route("/flag/admin/<string:username>/<int:campaign_id>/") 
def flag_camp_admin_page(username, campaign_id):

    campaign = CAMPAIGNS.query.filter_by(campaign_id = campaign_id).first()
    campaign.flagged = True
    database.session.commit()
    return redirect(url_for("find_admin_page", username = username))


@app.route("/search/admin/<string:username>/")
def search_admin(username):

    word = "%" + request.args.get("word") + "%"
    campaigns = CAMPAIGNS.query.filter(CAMPAIGNS.search.like(word)).all()
    influencers = INFLUENCERS.query.filter(INFLUENCERS.search.like(word)).all()
    sponsors = SPONSORS.query.filter(SPONSORS.search.like(word)).all()
    spons = SPONSORS.query.all()
    return render_template("admins/find.html", campaigns = campaigns, sponsors = sponsors, influencers = influencers, username = username, spons = spons)


# code ends
