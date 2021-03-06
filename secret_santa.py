import yaml
# sudo pip install pyyaml
import re
import random
import smtplib
import datetime
import pytz
import time
import socket
import sys
import getopt
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

help_message = '''
To use, fill out config.yml with your own participants. You can also specify 
DONT-PAIR so that people don't get assigned their significant other.

You'll also need to specify your mail server settings. An example is provided
for routing mail through gmail.

For more information, see README.
'''


msg1 = "<!doctype HTML public \"-//W3C//DTD HTML 4.0 Frameset//EN\"><html><head></head><body><div role=\"document\">  <div class=\"_rp_U4 _rp_V4 ms-font-weight-regular ms-font-color-neutralDark\" style=\"display: none;\"></div>  <div autoid=\"_rp_w\" class=\"_rp_U4\" style=\"display: none;\"></div>  <div autoid=\"_rp_x\" class=\"_rp_U4\" id=\"Item.MessagePartBody\" style=\"\"> <div class=\"_rp_V4 ms-font-weight-regular ms-font-color-neutralDark rpHighlightAllClass rpHighlightBodyClass\" id=\"Item.MessageUniqueBody\" style=\"font-family: &quot;wf_segoe-ui_normal&quot;, &quot;Segoe UI&quot;, &quot;Segoe WP&quot;, Tahoma, Arial, sans-serif, serif, &quot;EmojiFont&quot;;\"><div class=\"rps_b344\"><style type=\"text/css\"><!-- .rps_b344 body\
{ margin: 0; padding: 0; }\
.rps_b344 table, .rps_b344 tr, .rps_b344 td\
{ vertical-align: top; border-collapse: collapse; }\
.rps_b344 .x_ie-browser table, .rps_b344 .x_mso-container table\
{ table-layout: fixed; }\
.rps_b344 *\
{ line-height: inherit; }\
.rps_b344 ax_[x-apple-data-detectors=true]\
{ color: inherit!important; text-decoration: none!important; }\
.rps_b344 .x_img-container div, .rps_b344 .x_img-container button\
{ display: block!important; }\
.rps_b344 .x_fullwidth button\
{ width: 100%!important; }\
.rps_b344 .x_block-grid .x_col\
{ display: table-cell; float: none!important; vertical-align: top; }\
.rps_b344 .x_ie-browser .x_num12, .rps_b344 .x_ie-browser .x_block-grid, .rps_b344 .x_num12, .rps_b344 .x_block-grid\
{ width: 500px!important; }\
.rps_b344 .x_ExternalClass, .rps_b344 .x_ExternalClass p, .rps_b344 .x_ExternalClass span, .rps_b344 .x_ExternalClass font, .rps_b344 .x_ExternalClass td, .rps_b344 .x_ExternalClass div\
{ line-height: 100%; }\
.rps_b344 .x_ie-browser .x_mixed-two-up .x_num4, .rps_b344 .x_mixed-two-up .x_num4\
{ width: 164px!important; }\
.rps_b344 .x_ie-browser .x_mixed-two-up .x_num8, .rps_b344 .x_mixed-two-up .x_num8\
{ width: 328px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.two-up .x_col, .rps_b344 .x_block-grid.two-up .x_col\
{ width: 250px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.three-up .x_col, .rps_b344 .x_block-grid.three-up .x_col\
{ width: 166px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.four-up .x_col, .rps_b344 .x_block-grid.four-up .x_col\
{ width: 125px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.five-up .x_col, .rps_b344 .x_block-grid.five-up .x_col\
{ width: 100px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.six-up .x_col, .rps_b344 .x_block-grid.six-up .x_col\
{ width: 83px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.seven-up .x_col, .rps_b344 .x_block-grid.seven-up .x_col\
{ width: 71px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.eight-up .x_col, .rps_b344 .x_block-grid.eight-up .x_col\
{ width: 62px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.nine-up .x_col, .rps_b344 .x_block-grid.nine-up .x_col\
{ width: 55px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.ten-up .x_col, .rps_b344 .x_block-grid.ten-up .x_col\
{ width: 50px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.eleven-up .x_col, .rps_b344 .x_block-grid.eleven-up .x_col\
{ width: 45px!important; }\
.rps_b344 .x_ie-browser .x_block-grid.twelve-up .x_col, .rps_b344 .x_block-grid.twelve-up .x_col\
{ width: 41px!important; }\
 --></style>\
<div>\
<div class=\"x_clean-body\" style=\"margin:0; padding:0; background-color:#FFFFFF\">\
<div><img data-imagetype=\"External\" src=\"http://post.spmailtechnol.com/q/IoIzAcDGhz_-zukiM1tnxQ~~/AAISiQA~/RgRcAUSEPVcDc3BjWAQAAAAAQgoABYi_Hlq49Cw5QQgBbQ2r99HRJVkGc3dpcGlpYQZzd2lwaWlgDDM0LjIxMS4yNy4zOUgEMzcxOVIbaGFhcm9vbi55b3VzYWYuMTdAdWNsLmFjLnVrCVEEAAAAAEcUeyJlbWFpbF91aWQiOiIzNzE5In0~\" alt=\"\" width=\"1\" height=\"1\" border=\"0\"></div>\
<style type=\"text/css\"><!--  --></style>\
<table class=\"x_nl-container\" style=\"border-collapse:collapse; table-layout:fixed; border-spacing:0; vertical-align:top; min-width:320px; margin:0 auto; background-color:#FFFFFF; width:100%\" cellspacing=\"0\" cellpadding=\"0\">\
<tbody>\
<tr style=\"vertical-align:top\">\
<td style=\"word-break:break-word; border-collapse:collapse!important; vertical-align:top\">\
<div style=\"background-image:url('https://pro-bee-user-content-eu-west-1.s3.amazonaws.com/public/users/Integrators/64f54304-c721-42a6-a321-be83727879f4/rg-907/giphy%20%283%29.gif'); background-position:top left; background-repeat:repeat; background-color:#135700\">\
<div class=\"x_block-grid\" style=\"margin:0 auto; min-width:320px; max-width:500px; word-wrap:break-word; word-break:break-word; background-color:transparent\">\
<div style=\"border-collapse:collapse; display:table; width:100%; background-color:transparent\">\
<div class=\"x_col x_num12\" style=\"min-width:320px; max-width:500px; display:table-cell; vertical-align:top\">\
<div style=\"background-color:transparent; width:100%!important\">\
<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right:0px; padding-left:0px\">\
<div style=\"color: rgb(85, 85, 85); line-height: 120%; font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif, serif, &quot;EmojiFont&quot;; padding: 15px 10px;\">\
<div style=\"font-size: 12px; line-height: 14px; text-align: right; color: rgb(85, 85, 85); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif, serif, &quot;EmojiFont&quot;;\">\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:right\"><span style=\"color:rgb(153,153,153); font-size:12px; line-height:14px\">Feeling festive?</span></p>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
<div style=\"background-image:url('https://pro-bee-user-content-eu-west-1.s3.amazonaws.com/public/users/Integrators/64f54304-c721-42a6-a321-be83727879f4/rg-907/giphy%20%283%29.gif'); background-position:top left; background-repeat:repeat; background-color:#135700\">\
<div class=\"x_block-grid\" style=\"margin:0 auto; min-width:320px; max-width:500px; word-wrap:break-word; word-break:break-word; background-color:#FFFFFF\">\
<div style=\"border-collapse:collapse; display:table; width:100%; background-color:#FFFFFF\">\
<div class=\"x_col x_num12\" style=\"min-width:320px; max-width:500px; display:table-cell; vertical-align:top\">\
<div style=\"background-color:transparent; width:100%!important\">\
<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:15px; padding-bottom:10px; padding-right:10px; padding-left:10px\">\
<div class=\"x_img-container x_center x_autowidth x_fullwidth\" style=\"padding-right:0px; padding-left:0px\" align=\"center\">\
 </div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
<div style=\"background-image:url('https://pro-bee-user-content-eu-west-1.s3.amazonaws.com/public/users/Integrators/64f54304-c721-42a6-a321-be83727879f4/rg-907/giphy%20%283%29.gif'); background-position:top left; background-repeat:repeat; background-color:#135700\">\
<div class=\"x_block-grid\" style=\"margin:0 auto; min-width:320px; max-width:500px; word-wrap:break-word; word-break:break-word; background-color:#FFFFFF\">\
<div style=\"border-collapse:collapse; display:table; width:100%; background-color:#FFFFFF\">\
<div class=\"x_col x_num12\" style=\"min-width:320px; max-width:500px; display:table-cell; vertical-align:top\">\
<div style=\"background-color:transparent; width:100%!important\">\
<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right:0px; padding-left:0px\">\
<div class=\"x_img-container x_center x_autowidth x_fullwidth\" style=\"padding-right:0px; padding-left:0px\" align=\"center\">\
 </div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
<div style=\"background-image:url('https://pro-bee-user-content-eu-west-1.s3.amazonaws.com/public/users/Integrators/64f54304-c721-42a6-a321-be83727879f4/rg-907/giphy%20%283%29.gif'); background-position:top left; background-repeat:repeat; background-color:#135700\">\
<div class=\"x_block-grid x_mixed-two-up\" style=\"margin:0 auto; min-width:320px; max-width:500px; word-wrap:break-word; word-break:break-word; background-color:#FFFFFF\">\
<div style=\"border-collapse:collapse; display:table; width:100%; background-color:#FFFFFF\">\
<div class=\"x_col x_num8\" style=\"display:table-cell; vertical-align:top; min-width:320px; max-width:328px\">\
<div style=\"background-color:transparent; width:100%!important\">\
<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:15px; padding-bottom:15px; padding-right:15px; padding-left:15px\">\
\
</div>\
</div>\
</div>\
<div class=\"x_col x_num4\" style=\"display:table-cell; vertical-align:top; max-width:320px; min-width:164px\">\
<div style=\"background-color:transparent; width:100%!important\">\
<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:15px; padding-bottom:5px; padding-right:10px; padding-left:10px\">\
<div class=\"x_img-container x_center x_autowidth x_fullwidth\" style=\"padding-right:0px; padding-left:0px\" align=\"center\">\
 </div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
<div style=\"background-image:url('https://pro-bee-user-content-eu-west-1.s3.amazonaws.com/public/users/Integrators/64f54304-c721-42a6-a321-be83727879f4/rg-907/giphy%20%283%29.gif'); background-position:top left; background-repeat:repeat; background-color:#135700\">\
<div class=\"x_block-grid\" style=\"margin:0 auto; min-width:320px; max-width:500px; word-wrap:break-word; word-break:break-word; background-color:#FFFFFF\">\
<div style=\"border-collapse:collapse; display:table; width:100%; background-color:#FFFFFF\">\
<div class=\"x_col x_num12\" style=\"min-width:320px; max-width:500px; display:table-cell; vertical-align:top\">\
<div style=\"background-color:transparent; width:100%!important\">\
<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:30px; padding-right:0px; padding-left:0px\">\
<div style=\"color: rgb(85, 85, 85); line-height: 120%; font-family: &quot;Roboto&quot;, Tahoma, Verdana, Segoe, sans-serif, serif, &quot;EmojiFont&quot;; padding: 10px;\">\
<div style=\"font-size: 12px; line-height: 14px; font-family: Roboto, Tahoma, Verdana, Segoe, sans-serif, serif, &quot;EmojiFont&quot;; color: rgb(85, 85, 85); text-align: left;\">\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"><img src=\"https://images.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.oPm270H1AIkrH0a8ejs9kAEsDh%26pid%3D15.1&amp;f=1\" alt=\"xmas-cat\" <=\"\" span=\"\" width=\"350\" height=\"250\"></span></p><p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"><br>\
</span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>"

msg2 = "<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">Dear {santa},</span></p>\
\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"><br>\
</span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">This year you are {santee}'s Secret Santa!.</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">Indeed you may have lots of banter!.</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">The speding limit is 10 British Pounds,</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">Ensure your gift is between the bounds.</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">Be mindful of {santee}'s beliefs.</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">Don't trigger any allergies or cause mischiefs.</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">This message was automagically sent from a computer.</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">I know, it couldn't be any cuter ^_^</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">So keep within the holiday cheer,</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">or you'll turn into a laughing deer.</span><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\"></span></p>"

msg3 = "<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\">&nbsp;<br>\
</p>\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:center\"><span style=\"font-size:14px; line-height:16px; color:rgb(51,51,51)\">:)</span></p>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
<div style=\"background-image:url('https://pro-bee-user-content-eu-west-1.s3.amazonaws.com/public/users/Integrators/64f54304-c721-42a6-a321-be83727879f4/rg-907/giphy%20%283%29.gif'); background-position:top left; background-repeat:repeat; background-color:#135700\">\
<div class=\"x_block-grid\" style=\"margin:0 auto; min-width:320px; max-width:500px; word-wrap:break-word; word-break:break-word; background-color:#135700\">\
<div style=\"border-collapse:collapse; display:table; width:100%; background-color:#135700\">\
<div class=\"x_col x_num12\" style=\"min-width:320px; max-width:500px; display:table-cell; vertical-align:top\">\
\
</div>\
</div>\
</div>\
</div>\
<div style=\"background-image:url('https://pro-bee-user-content-eu-west-1.s3.amazonaws.com/public/users/Integrators/64f54304-c721-42a6-a321-be83727879f4/rg-907/giphy%20%283%29.gif'); background-position:top left; background-repeat:repeat; background-color:#135700\">\
<div class=\"x_block-grid\" style=\"margin:0 auto; min-width:320px; max-width:500px; word-wrap:break-word; word-break:break-word; background-color:transparent\">\
<div style=\"border-collapse:collapse; display:table; width:100%; background-color:transparent\">\
<div class=\"x_col x_num12\" style=\"min-width:320px; max-width:500px; display:table-cell; vertical-align:top\">\
<div style=\"background-color:transparent; width:100%!important\">\
<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right:0px; padding-left:0px\">\
<div style=\"color: rgb(85, 85, 85); line-height: 120%; font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif, serif, &quot;EmojiFont&quot;; padding: 15px 10px;\">\
<div style=\"font-size: 12px; line-height: 14px; text-align: right; color: rgb(85, 85, 85); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif, serif, &quot;EmojiFont&quot;;\">\
<p style=\"margin:0; font-size:12px; line-height:14px; text-align:right\"><span style=\"color:rgb(153,153,153); font-size:12px; line-height:14px\">Feeling festive?</span></p>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</div>\
</td>\
</tr>\
</tbody>\
</table>\
<img data-imagetype=\"External\" src=\"http://post.spmailtechnol.com/q/cFsh9ItsIlj4PV75FZbzqQ~~/AAISiQA~/RgRcAUSEPlcDc3BjWAQAAAAAQgoABYi_Hlq49Cw5QQgBbQ2r99HRJVkGc3dpcGlpYQZzd2lwaWlgDDM0LjIxMS4yNy4zOUgEMzcxOVIbaGFhcm9vbi55b3VzYWYuMTdAdWNsLmFjLnVrCVEEAAAAAEcUeyJlbWFpbF91aWQiOiIzNzE5In0~\" alt=\"\" width=\"1\" height=\"1\" border=\"0\"> </div>\
\
</div>\
</div></div> <div style=\"display: none;\" class=\"_rp_d5\"></div> </div>  <span class=\"PersonaPaneLauncher\"><div ariatabindex=\"-1\" class=\"_pe_d _pe_62\" aria-expanded=\"false\" tabindex=\"-1\" aria-haspopup=\"false\">  <div style=\"display: none;\"></div> </div></span> </div></body></html>"

REQRD = (
    'SMTP_SERVER', 
    'SMTP_PORT', 
    'USERNAME', 
    'PASSWORD', 
    'TIMEZONE', 
    'PARTICIPANTS', 
    # 'DONT-PAIR',
    'FROM', 
    'SUBJECT', 
    'MESSAGE',
)

HEADER = """Date: {date}
Content-Type: text/plain; charset="utf-8"
Message-Id: {message_id}
From: {frm}
To: {to}
Subject: {subject}
"""

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')

class Person:
    def __init__(self, name, email, invalid_matches):
        self.name = name
        self.email = email
        self.invalid_matches = invalid_matches
    
    def __str__(self):
        return "%s <%s>" % (self.name, self.email)

class Pair:
    def __init__(self, giver, reciever):
        self.giver = giver
        self.reciever = reciever
    
    def __str__(self):
        return "%s ---> %s" % (self.giver.name, self.reciever.name)

def parse_yaml(yaml_path=CONFIG_PATH):
    return yaml.load(open(yaml_path))    

def choose_reciever(giver, recievers):
    choice = random.choice(recievers)
    if choice.name in giver.invalid_matches or giver.name == choice.name:
        if len(recievers) is 1:
            raise Exception('Only one reciever left, try again')
        return choose_reciever(giver, recievers)
    else:
        return choice

def create_pairs(g, r):
    givers = g[:]
    recievers = r[:]
    pairs = []
    for giver in givers:
        try:
            reciever = choose_reciever(giver, recievers)
            recievers.remove(reciever)
            pairs.append(Pair(giver, reciever))
        except:
            return create_pairs(g, r)
    return pairs


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "shc", ["send", "help"])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        send = False
        for option, value in opts:
            if option in ("-s", "--send"):
                send = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
                
        config = parse_yaml()
        for key in REQRD:
            if key not in config.keys():
                raise Exception(
                    'Required parameter %s not in yaml config file!' % (key,))

        participants = config['PARTICIPANTS']
        # dont_pair = config['DONT-PAIR']
        if len(participants) < 2:
            raise Exception('Not enough participants specified.')
        
        givers = []
        for person in participants:
            name, email = re.match(r'([^<]*)<([^>]*)>', person).groups()
            name = name.strip()
            invalid_matches = []
            # for pair in dont_pair:
            #     names = [n.strip() for n in pair.split(',')]
            #     if name in names:
            #         # is part of this pair
            #         for member in names:
            #             if name != member:
            #                 invalid_matches.append(member)
            person = Person(name, email, invalid_matches)
            givers.append(person)
        
        recievers = givers[:]
        pairs = create_pairs(givers, recievers)
        if not send:
            print """
Test pairings:
                
%s
                
To send out emails with new pairings,
call with the --send argument:

    $ python secret_santa.py --send
            
            """ % ("\n".join([str(p) for p in pairs]))
        
        if send:
            server = smtplib.SMTP(config['SMTP_SERVER'], config['SMTP_PORT'])
            server.starttls()
            server.login(config['USERNAME'], config['PASSWORD'])
        for pair in pairs:
            zone = pytz.timezone(config['TIMEZONE'])
            now = zone.localize(datetime.datetime.now())
            date = now.strftime('%a, %d %b %Y %T %Z') # Sun, 21 Dec 2008 06:25:23 +0000
            message_id = '<%s@%s>' % (str(time.time())+str(random.random()), socket.gethostname())
            frm = config['FROM']
            to = pair.giver.email
            subject = config['SUBJECT'].format(santa=pair.giver.name, santee=pair.reciever.name)
#             message = "\n\nDear {santa},\n\n\
# This year you are {santee}'s Secret Santa!.\n\
# Indeed you may have lots of banter.\n\n\
# The speding limit is 10 British Pounds.\n\
# Ensure your gift is between the bounds.\n\n\
# Be mindful of {santee}'s beliefs.\n\
# Don't trigger any allergies or cause mischiefs.\n\n\
# This message was automagically sent from a computer.\n\
# I know, it couldn't be any cuter ^_^\n\n\
# So keep within the holiday cheer,\n\
# or you'll turn into a laughing deer.\n\n:)\n\n"
            temp = msg2
            temp = temp.format(
                santa=pair.giver.name,
                santee=pair.reciever.name,
            )
            temp = msg1+temp+msg3
            tempHeader = HEADER+""
            # header2 = tempHeader.format(
            #     date=date,
            #     message_id=message_id,
            #     frm=frm,
            #     to=to,
            #     subject=subject
            # )
            body = temp
            #print body
            msg = MIMEMultipart('alternative')
            msg["Date"] = date
            msg['Subject'] = subject
            msg['From'] = frm
            msg['To'] = to
            part2 = MIMEText(body, 'html')
            msg.attach(part2)
            if send:
                result = server.sendmail(frm, [to], msg.as_string())
                print "Emailed %s <%s>" % (pair.giver.name, to)

        if send:
            server.quit()
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())