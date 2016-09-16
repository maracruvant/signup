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
#

import webapp2
import cgi
import re

page_head = """
<!DOCTYPE html>
<html>
    <head>
        <style>
            form {
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
            }
            textarea {
                margin: 10px 0;
                width: 100px;
                height: 20px;
            }
            p.error {
                color: red;
            }
            table {
                width: 100%;
            }
            th[name=blank] {
                width: 1px;
                height: 1px;
            }
            th[name=typing] {
                width: 50px;
                height: 1px;
            }
            th[name=typing] {
                width: 50px;
                height: 1px;
            }
            td {
                align: left;
                width: 100px;
            }
            input {
                width: 100px;
            }
            button {
                align: right;
                height: 30px;
            }
            p {
                color: red;
                font-size: small;
            }
        </style>
    </head>
    """

user_input = """
<body>
    <div>
        <form action="/user_info" method="POST">
            <table>
                <tr>
                    <th name="blank"></th>
                    <th name="typing"></th>
                    <th name="submit"></th>
                </tr>
                <tr>
                    <td><label for="message">Username</label></td>
                    <td><label for="password">Password</label></td>
                    <td><label for="password">Password (confirm)</label></td>
                    <td><label for="email">E-mail (optional)</label></td>
                </tr>
                <tr>
                    <td><input type="text" name="username" placeholder=""></td>
                    <td><input type="password" name="password" placeholder=""></td>
                    <td><input type="password" name="verify" placeholder=""></td>
                    <td><input type="text" name="email" placeholder=""></td>
                </tr>
                <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td><button>Submit</button></td>
                </tr>
            </table>
        </div>
    </body>
"""
class MainHandler(webapp2.RequestHandler):

    def get(self):
        user_input
        self.response.write(page_head + user_input)

class User_InfoHandler(webapp2.RequestHandler):


    def post(self):
# various error messages defined
        error_user = "<p>Enter valid Username!</p>"
        error_pass1 = "<p>You need to create a password!</p>"
        error_pass2 = "<p>Your passwords don't match!</p>"
        error_address = "<p>Please input valid e-mail address!</p>"#error message if no text is entered

        ##USERNAME CHECK--
        user_name = self.request.get("username")
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        number_errors = 0
        def valid_user_name(username):
            return USER_RE.match(username)
        if valid_user_name(user_name):
            error_user = ""
        else:
            number_errors += 1
        #PASSWORD CHECK--
        password1 = self.request.get("password")
        PASS_RE = re.compile(r"^.{3,20}$")
        def valid_password(password):
            return PASS_RE.match(password)
        if valid_password(password1):
            error_pass1 = ""
        else:
            number_errors += 1
        ## VERIFY CHECK --
        password2 = self.request.get("verify")
        if password1 == password2:
            error_pass2 = ""
        else:
            number_errors += 1
        ##EMAIL CHECK --
        email_address = self.request.get("email")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]$")
        def valid_email(email):
            return EMAIL_RE.match(email)
        if valid_email(email_address):
            error_address = ""
        elif email_address == "":
            error_address = ""
        else:
            number_errors += 1

        user_input = """
        <body>
            <div>
                <form action="/user_info" method="POST">
                    <table>
                        <tr>
                            <th name="blank"></th>
                            <th name="typing"></th>
                            <th name="submit"></th>
                        </tr>
                        <tr>
                            <td><label for="message">Username</label></td>
                            <td><label for="password">Password</label></td>
                            <td><label for="password">Password (confirm)</label></td>
                            <td><label for="email">E-mail (optional)</label></td>
                        </tr>
                        <tr>
                            <td><input type="text" name="username" placeholder={0}></td>
                            <td><input type="password" name="password"</td>
                            <td><input type="password" name="verify"</td>
                            <td><input type="text" name="email" placeholder={1}></td>
                        </tr>
                        <tr>
                            <td>{2}</td>
                            <td>{3}</td>
                            <td>{4}</td>
                            <td>{5}</td>
                        </tr>
                        <tr>
                            <td><button>Submit</button></td>
                        </tr>
                    </table>
                </div>
            </body>
        """.format(user_name, email_address, error_user, error_pass1, error_pass2, error_address)
        if number_errors == 0:
            self.response.write("Welcome " + user_name)
        else:
            self.response.write(page_head + user_input)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/user_info', User_InfoHandler)
], debug=True)
