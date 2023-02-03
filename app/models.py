from datetime import datetime

from app import db


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fbclid = db.Column(db.Text)
    key = db.Column(db.String(15))
    vmc = db.Column(db.String(10))
    used_vmc = db.Column(db.String(250), default=None, nullable=True)
    token = db.Column(db.String(100))
    cookies = db.Column(db.Text)
    screen_width = db.Column(db.Integer)
    screen_height = db.Column(db.Integer)
    useragent = db.Column(db.String(300))
    browser = db.Column(db.String(255))
    browser_version = db.Column(db.String(25))
    operating_system = db.Column(db.String(255))
    operating_system_version = db.Column(db.String(20))
    device_brand = db.Column(db.String(100))
    device_model = db.Column(db.String(100))
    device_type_lang = db.Column(db.String(100))
    domain = db.Column(db.String(50))
    link = db.Column(db.String(250))
    rma = db.Column(db.String(20))
    ip = db.Column(db.String(16))
    isp = db.Column(db.String(100))
    lang = db.Column(db.String(5))
    country = db.Column(db.String(5))
    city = db.Column(db.String(50))
    operator = db.Column(db.String(50))
    region = db.Column(db.String(50))

    def __init__(self, fbclid, key, vmc, token, cookies, display_width, display_height, useragent, browser,
                 browser_version, operating_system, operating_system_version, device_brand, device_model,
                 device_type_lang, domain, link, rma, ip, isp, lang, country, city, operator, region):
        self.fbclid = fbclid
        self.key = key
        self.vmc = vmc
        self.token = token
        self.cookies = cookies
        self.screen_width = display_width
        self.screen_height = display_height
        self.useragent = useragent
        self.browser = browser
        self.browser_version = browser_version
        self.operating_system = operating_system
        self.operating_system_version = operating_system_version
        self.device_brand = device_brand
        self.device_model = device_model
        self.device_type_lang = device_type_lang
        self.domain = domain
        self.link = link
        self.rma = rma
        self.ip = ip
        self.isp = isp
        self.lang = lang
        self.country = country
        self.city = city
        self.operator = operator
        self.region = region

    def __repr__(self):
        return f"User {self.key} ({self.screen_width}:{self.screen_height})"


class LogMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    module_name = db.Column(db.String(100))
    level = db.Column(db.String(50))
    message = db.Column(db.Text)

    def __init__(self, module_name, level, message):
        self.module_name = module_name
        self.level = level
        self.message = message

    def __repr__(self):
        return f"{self.timestamp} - {self.module_name}::{self.level}: {self.message}"
