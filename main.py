#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#http://localhost:8080/Leaderboard
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

"""
Helper Classes Go Below Here:
"""
ALL_USERS = 'user_container'


def user_key(parent_user=ALL_USERS):
    """Constructs a Datastore key for a Guestbook entity with parent_user."""
    return ndb.Key('ParentUser', parent_user)


class UserEntry(ndb.Model):
    """Models an individual Guestbook entry with alias, emailaddress, and date."""
    points = ndb.IntegerProperty(default=0)
    possiblepoints = ndb.IntegerProperty(default=0)
    nickname = ndb.StringProperty(indexed=False)
    emailaddress = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
"""
Particular Webpage Classes Go below here:
"""
class EntryPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('Main.html')
        self.response.write(template.render())

class PhishedPage(webapp2.RequestHandler):
    def get(self):
        idnum = self.request.get('idnum', '')
        parent_user = ALL_USERS
        luckyuser = UserEntry.get_by_id(int(idnum),parent=user_key(parent_user))
        luckyuser.points = luckyuser.points+1
        luckyuser.put()

        template = JINJA_ENVIRONMENT.get_template('PHISHED.html')
        self.response.write(template.render())

class MoreInfoPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('moreinfo.html')
        self.response.write(template.render())

class IntroductionPage(webapp2.RequestHandler):
    def get(self):

        parent_user = ALL_USERS

        appUser = UserEntry(parent=user_key(parent_user))

        if users.get_current_user():
            currentUser = users.get_current_user()
            parent_user = ALL_USERS
            user_query = UserEntry.query(ancestor=user_key(parent_user)).filter(ndb.StringProperty('emailaddress')==currentUser.email())
            if len(user_query.fetch(1)) == 0:
                appUser.emailaddress = currentUser.email()
                appUser.nickname = currentUser.nickname()
                appUser.put()

            

            logUrl = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            logUrl = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'logUrl': logUrl,
            'url_linktext': url_linktext,
            }

        template = JINJA_ENVIRONMENT.get_template('Home.html')
        self.response.write(template.render(template_values))

class AliasSelectionPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('AliasSelection.html')
        self.response.write(template.render())

    def post(self):
        pass

class AmmazonTemplateEditingPage(webapp2.RequestHandler):
    def get(self):

        defaultTemplate = "We regret to inform you that your current order is has been significantly delayed. \nIn order to compensate you for your inconvience we are applying a $50 credit to your account. To confirm this addition click the following link"
        template_values = {
        'defaultTemplate' : defaultTemplate
        }

        template = JINJA_ENVIRONMENT.get_template('AmmazonTemplateEditingPage.html', template_values)
        self.response.write(template.render(template_values))


class BanOfAmericaTemplateEditingPage(webapp2.RequestHandler):
    def get(self):
        defaultTemplate = "There has been suspicious activity on your checking account. \nIn order to verify your recent transaction history please click on the link below"
        template_values = {
        'defaultTemplate' : defaultTemplate
        }
        template = JINJA_ENVIRONMENT.get_template('BanOfAmericaTemplateEditingPage.html', template_values)
        self.response.write(template.render(template_values))

class FeddexTemplateEditingPage(webapp2.RequestHandler):
    def get(self):

        defaultTemplate = "We regret to inform you that your current order is has been significantly delayed. \nClick the following link to see your updated package tracking"
        template_values = {
        'defaultTemplate' : defaultTemplate
        }

        template = JINJA_ENVIRONMENT.get_template('FeddexTemplateEditingPage.html', template_values)
        self.response.write(template.render(template_values))

class EbayeTemplateEditingPage(webapp2.RequestHandler):
    def get(self):

        defaultTemplate = "We regret to inform you that your current order is has been significantly delayed. \nClick the following link to see your updated package tracking"
        template_values = {
        'defaultTemplate' : defaultTemplate
        }

        template = JINJA_ENVIRONMENT.get_template('EbayeTemplateEditingPage.html', template_values)
        self.response.write(template.render(template_values))

class CitiyBankTemplateEditingPage(webapp2.RequestHandler):
    def get(self):

        defaultTemplate = "There has been suspicious activity on your checking account. \nIn order to verify your recent transaction history please click on the link below"
        template_values = {
        'defaultTemplate' : defaultTemplate
        }

        template = JINJA_ENVIRONMENT.get_template('CitiyTemplateEditingPage.html', template_values)
        self.response.write(template.render(template_values))

class ChaeseBankTemplateEditingPage(webapp2.RequestHandler):
    def get(self):

        defaultTemplate = "There has been suspicious activity on your checking account. \nIn order to verify your recent transaction history please click on the link below"
        template_values = {
        'defaultTemplate' : defaultTemplate
        }

        template = JINJA_ENVIRONMENT.get_template('ChaeseTemplateEditingPage.html', template_values)
        self.response.write(template.render(template_values))

class USPSSTemplateEditingPage(webapp2.RequestHandler):
    def get(self):

        defaultTemplate = "We regret to inform you that your current order is has been significantly delayed. \nClick the following link to see your updated package tracking"
        template_values = {
        'defaultTemplate' : defaultTemplate
        }

        template = JINJA_ENVIRONMENT.get_template('FeddexTemplateEditingPage.html', template_values)
        self.response.write(template.render(template_values))

class LeaderboardPage(webapp2.RequestHandler):

    def get(self):

        parent_user = ALL_USERS
        users_query = UserEntry.query(ancestor=user_key(parent_user)).order(-UserEntry.points)
        users = users_query.fetch(10)
        leaderboard={}


        i = 1
        for highuser in users:
            leaderboard[i] = {} 
            leaderboard[i]['Nickname'] = highuser.nickname
            leaderboard[i]['Points'] = highuser.points
            i = i+1

        template_values={
        "leaderboard":leaderboard
        }

        template = JINJA_ENVIRONMENT.get_template('Leaderboard.html')
        self.response.write(template.render(template_values))

    def post(self):

        currentUser = users.get_current_user()
        parent_user = ALL_USERS
        user_query = UserEntry.query(ancestor=user_key(parent_user)).filter(ndb.StringProperty('emailaddress')==currentUser.email())
        id = user_query.fetch(1)[0]._key.id()
        newurl = "\n<a href=\"http://phishyourfriends.appspot.com/Phished?idnum="+ str(id)+"\">Click Here to Proceed </a>" 

        finalEmail = self.request.get("finalTemplate")
        recipients = self.request.get("recipients").split(',')
        alias      = self.request.get("alias")

        def ammazon():
            subject = "Delayed Package"
            sender_address = "Ammazon.User.Help@gmail.com"
            emailInfo = [sender_address,subject]
            return emailInfo

        def banOfAmerica():
            subject = "suspicious Account Acjtivity"
            sender_address = "BanOfAmerica.User.Help@gmail.com"
            emailInfo = [sender_address,subject]
            return emailInfo

        def feddex():
            subject = "Delayed Package"
            sender_address = "Feddex.User.Help@gmail.com"
            emailInfo = [sender_address,subject]
            return emailInfo

        def uspss():
            subject = "Delayed Package"
            sender_address = "uspss.User.Help@gmail.com"
            emailInfo = [sender_address,subject]
            return emailInfo

        def ebaye():
            subject = "Delayed Package"
            sender_address = "Ebaye.User.Help@gmail.com"
            emailInfo = [sender_address,subject]
            return emailInfo

        def chaeseBank():
            subject = "suspicious Account Acjtivity"
            sender_address = "ChaeseBank.User.Help@gmail.com"
            emailInfo = [sender_address,subject]
            return emailInfo

        def citiyBank():
            subject = "suspicious Account Acjtivity"
            sender_address = "citiyBank.User.Help@gmail.com"
            emailInfo = [sender_address,subject]
            return emailInfo


        options = {"ammazon" : ammazon,
                   "banOfAmerica" : banOfAmerica,
                   "feddex" : feddex,
                   "uspss" : uspss,
                   "ebaye" : ebaye
                   "citiyBank" : citiyBank,
                   "chaeseBank" : chaesBank
                   }

        emailInfo = options[alias]()


        for recipient in recipients:
          
            mail.send_mail(emailInfo[0], recipient, emailInfo[1],'', html=finalEmail+newurl)

        self.redirect("/Leaderboard")

application = webapp2.WSGIApplication([
    ('/', EntryPage),
    ('/Intro', IntroductionPage),
    ('/MoreInfo', MoreInfoPage),
    ('/AliasSelection', AliasSelectionPage),
    ('/TemplateEditing/Ammazon', AmmazonTemplateEditingPage),
    ('/TemplateEditing/BanOfAmerica', BanOfAmericaTemplateEditingPage),
    ('TemplateEditing/Feddex',FeddexTemplateEditingPage),
    ('TemplateEditing/Ebaye', EbayeTemplateEditingPage),
    ('TemplateEditing/CitiyBank'CitiyBankTemplateEditingPage),
    ('TemplateEditing/ChaeseBank',ChaeseBankTemplatEditingPage),
    ('TemplateEditing/USPSS', USPSSTemplateEditingPage),
    ('/Phished', PhishedPage),
    ('/Leaderboard', LeaderboardPage)
], debug=True)
