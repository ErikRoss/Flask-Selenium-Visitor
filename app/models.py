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


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_type = db.Column(db.String(100))
    priority = db.Column(db.Integer, default=0)
    param_name = db.Column(db.String(100), nullable=True)
    param_value = db.Column(db.String(255), nullable=True)
    algorithm_id = db.Column(db.Integer, db.ForeignKey('algorithm.id'))
    creator = db.Column(db.Integer, default=0)

    def __init__(self, rule_type, priority, param_name, param_value, algorithm, creator):
        self.rule_type = rule_type
        self.priority = priority
        self.param_name = param_name
        self.param_value = param_value
        self.algorithm_id = algorithm
        self.creator = creator

    def __repr__(self):
        return f"{self.param_name}: {self.param_value}"


class Algorithm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rules = db.relationship('Rule', backref='algorithm', lazy=True)
    lvl_1 = db.Column(db.String(255), nullable=True)
    lvl_2 = db.Column(db.String(255), nullable=True)
    lvl_3 = db.Column(db.String(255), nullable=True)
    lvl_4 = db.Column(db.String(255), nullable=True)
    lvl_5 = db.Column(db.String(255), nullable=True)
    lvl_6 = db.Column(db.String(255), nullable=True)
    lvl_7 = db.Column(db.String(255), nullable=True)
    lvl_8 = db.Column(db.String(255), nullable=True)
    lvl_9 = db.Column(db.String(255), nullable=True)
    lvl_10 = db.Column(db.String(255), nullable=True)
    uses_1 = db.Column(db.Integer, default=0)
    uses_2 = db.Column(db.Integer, default=0)
    uses_3 = db.Column(db.Integer, default=0)
    uses_4 = db.Column(db.Integer, default=0)
    uses_5 = db.Column(db.Integer, default=0)
    uses_6 = db.Column(db.Integer, default=0)
    uses_7 = db.Column(db.Integer, default=0)
    uses_8 = db.Column(db.Integer, default=0)
    uses_9 = db.Column(db.Integer, default=0)
    uses_10 = db.Column(db.Integer, default=0)

    def __init__(self, lvl_1=None, lvl_2=None, lvl_3=None, lvl_4=None, lvl_5=None, lvl_6=None, lvl_7=None,
                 lvl_8=None, lvl_9=None, lvl_10=None):
        self.lvl_1 = lvl_1
        self.lvl_2 = lvl_2
        self.lvl_3 = lvl_3
        self.lvl_4 = lvl_4
        self.lvl_5 = lvl_5
        self.lvl_6 = lvl_6
        self.lvl_7 = lvl_7
        self.lvl_8 = lvl_8
        self.lvl_9 = lvl_9
        self.lvl_10 = lvl_10

    def __repr__(self):
        return f"Algorithm {self.id}: Param 1: {self.lvl_1}, Param 2: {self.lvl_2}, Param 3: {self.lvl_3}, " \
               f"Param 4: {self.lvl_4}, Param 5: {self.lvl_5}, Param 6: {self.lvl_6}, Param 7: {self.lvl_7}, " \
               f"Param 8: {self.lvl_8}, Param 9: {self.lvl_9}, Param 10: {self.lvl_10}"
