# for key, value in request.args.items():
# pass
import json
import logging
import traceback
import re
from urllib.parse import unquote

from flask import request, render_template

from app import app, db, page_visitor
from app.models import UserInfo, LogMessage, Rule, Algorithm

logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(message)s')


def save_log(module_name, level, message):
    """
    Запись логов в БД

    :param module_name: Модуль-источник
    :param level: Уровень сообщения
    :param message: Текст сообщения
    """
    log_entry = LogMessage(module_name, level, message)
    db.session.add(log_entry)
    db.session.commit()


@app.template_filter('from_json')
def from_json_filter(value):
    return json.loads(value)


@app.route('/save', methods=['GET', 'POST'])
def save():
    """
    Разбор параметров POST-запроса и сохранение данных о посещении страницы

    :return: Результат записи в БД
    """
    if request.method == 'POST':
        try:
            user_data = request.form
            save_log("Save", "INFO", "Got user data: \n" + str(user_data))
            if user_data:
                print(user_data)
                if user_data["key"]:
                    key = user_data["key"]
                else:
                    key = ""
                if key == "" or key is None:
                    save_log("Save", "ERROR", "Cant create user with empty key")
                    return "Can't create user info without key"
                if user_data["fbclid"]:
                    fbclid = user_data["fbclid"]
                else:
                    fbclid = ""
                if user_data["vmc"]:
                    vmc = user_data["vmc"]
                else:
                    vmc = ""
                if user_data["token"]:
                    token = user_data["token"]
                else:
                    token = ""
                if user_data["cookies"]:
                    cookies = user_data["cookies"]
                else:
                    cookies = ""
                if user_data["screen[width]"]:
                    screen_width = int(user_data["screen[width]"])
                    print(f"screen_width: {screen_width}")
                else:
                    screen_width = 0
                if user_data["screen[height]"]:
                    screen_height = int(user_data["screen[height]"])
                    print(f"screen_height: {screen_height}")
                else:
                    screen_height = ""
                if user_data["useragent"]:
                    useragent = unquote(user_data["useragent"]).replace("+", " ")
                else:
                    useragent = ""
                if user_data["browser"]:
                    browser = user_data["browser"].replace("+", " ")
                else:
                    browser = ""
                if user_data["browser_ver"]:
                    browser_ver = user_data["browser_ver"]
                else:
                    browser_ver = ""
                if user_data["os"]:
                    os_ = user_data["os"].replace("+", " ")
                else:
                    os_ = ""
                if user_data["os_version"]:
                    os_version = user_data["os_version"]
                else:
                    os_version = ""
                if user_data["domain"]:
                    domain = user_data["domain"]
                else:
                    domain = ""
                if user_data["link"]:
                    link = user_data["link"]
                else:
                    link = ""
                if user_data["rma"]:
                    rma = user_data["rma"]
                else:
                    rma = ""
                if user_data["device_brand"]:
                    device_brand = user_data["device_brand"]
                else:
                    device_brand = ""
                if user_data["device_model"]:
                    device_model = user_data["device_model"].replace("+", " ")
                else:
                    device_model = ""
                if user_data["device_type_lang"]:
                    device_type_lang = user_data["device_type_lang"].replace("+", " ")
                else:
                    device_type_lang = ""
                if user_data["ip"]:
                    ip = user_data["ip"]
                else:
                    ip = ""
                if user_data["isp"]:
                    isp = user_data["isp"]
                else:
                    isp = ""
                if user_data["lang"]:
                    lang = user_data["lang"]
                else:
                    lang = ""
                if user_data["country"]:
                    country = user_data["country"]
                else:
                    country = ""
                if user_data["city"]:
                    city = user_data["city"].replace("+", " ")
                else:
                    city = ""
                if user_data["operator"]:
                    operator = user_data["operator"]
                else:
                    operator = ""
                if user_data["region"]:
                    region = user_data["region"]
                else:
                    region = ""
                user_info = UserInfo(fbclid, key, vmc, token, cookies, screen_width, screen_height, useragent, browser,
                                     browser_ver, os_, os_version, device_brand, device_model, device_type_lang, domain,
                                     link, rma, ip, isp, lang, country, city, operator, region)
                print(user_info)
                db.session.add(user_info)
                db.session.commit()
                if user_info.id is not None:
                    save_log("Save", "INFO", f"User {key} successfully created with ID {user_info.id}")
                    return f"User {key} successfully saved."
                else:
                    save_log("Save", "ERROR",
                             f"Got some error while creating user with key {key}. (Source link: {user_info.link})")
            else:
                save_log("Save", "ERROR", f"Got error parsing user info")
                return f"Error parsing user info"
        except Exception:
            save_log("Save", "ERROR", f"Got error parsing & saving user info: {traceback.format_exc()}")
    else:
        save_log("Save", "ERROR", f"Got GET request instead of POST")
        return "<html><body><h1>WEBSERVICE</h1></body></html>"


@app.route("/emulate", methods=['POST'])
def emulate():
    """
    Эмуляция посещения страницы через Selenium

    :return: Успех/Неудача посещения страницы
    """

    def check_vmc(user, value):
        """
        Проверка, был ли ранее использован пользователем указанный vmc

        :param user: проверяемый пользователь
        :param value: значение vmc

        :return: False - не был использован, True - был использован
        """
        if user.used_vmc is None:
            return False
        else:
            if value in user.used_vmc.split(","):
                return True
            else:
                return False

    def save_vmc(user, value):
        """
        Сохранение использованного при посещении страницы vmc за пользователем

        :param user: объект пользователя, которому присваивается полученный vmc
        :param value: значение vmc
        """
        if user.used_vmc is None:
            user.used_vmc = value
        else:
            user.used_vmc += f",{value}"
        db.session.commit()

    def get_keys(request_args=None):
        key = request_args.get('key')
        vmc = request_args.get('vmc')
        xcn = request_args.get('xcn')
        save_log("Emulate", "INFO", f"Got parameters: key={key}, vmc={vmc}, xcn={xcn}")
        logging.info(f"Got parameters: key={key}, vmc={vmc}, xcn={xcn}")
        if key is None or vmc is None or xcn is None:
            return None
        else:
            return {"key": key, "vmc": vmc, "xcn": xcn}

    def make_visit(keys):
        user_data = UserInfo.query.filter(UserInfo.key == keys["key"]).first()
        logging.info(f"Found User: {user_data}")
        if user_data is not None:
            save_log("Emulate", "INFO", f"Found User: {user_data}")
            if check_vmc(user_data, keys["vmc"]) is False:
                visit = page_visitor.Browser().visit_page(user_data, vmc=keys["vmc"], xcn=keys["xcn"])
                if visit is True:
                    save_log("Emulate", "INFO", f"User {keys['key']} successfully visited page.")
                    save_vmc(user_data, keys["vmc"])
                    return "Page successfully visited."
                else:
                    save_log("Emulate", "ERROR", f"User {keys['key']} not visited page. (Source link: {user_data.link}")
                    return "Page not visited."
            else:
                save_log("Emulate", "ERROR",
                         f"User {keys['key']} not visited page. This vmc ({keys['vmc']}) is already used.")
                return f"Page not visited. This vmc ({keys['vmc']}) is already used."
        else:
            save_log("Emulate", "ERROR", f"Can't visit page: User not found.")
            return "User not found."

    keys_dict = get_keys(request.args)
    if keys_dict is not None:
        return make_visit(keys_dict)
    else:
        save_log("Emulate", "ERROR", "Can't visit page: required parameters are missing")
        return "Page not visited."


@app.route("/show_all", methods=['GET', 'POST'])
def show_all():
    """
    Вывод на страницу краткой информации о пользователях, сохранённых в БД

    :return: Страница с таблицей пользователей
    """
    # UserInfo.query.delete()
    all_users = UserInfo.query.all()
    userslist = ""
    for user in all_users:
        userslist += "<p>" + str(user) + "</p>" + "<p>" + str(user.cookies) + "</p>"
        print(user.cookies)
    return f"<html><body>{userslist}</body></html>"


@app.route("/show_log/<int:limit>", methods=['GET', 'POST'])
@app.route("/show_log/", methods=['GET', 'POST'])
@app.route("/show_log", methods=['GET', 'POST'])
def show_log(limit=20):
    """
    Вывод логов работы на страницу в форме таблицы

    :return: Страница с таблицей записей лога
    """
    logs = LogMessage.query.order_by(-LogMessage.id).limit(limit)
    return render_template("logs.html", logs=logs)


def get_algorithm_parameters(alg):
    parameters = []
    for i in range(1, 11):
        key_name = None
        for key in alg.keys():
            match = re.search(r'\d+', key)
            if match and int(match.group()) == i:
                key_name = key
                break
        if key_name is None:
            value = alg.get(str(i))
        else:
            value = alg.get(key_name)
            value["name"] = key_name
            value["stopped"] = False
        print(f"Value for key {key_name}: {value}")
        parameters.append(json.dumps(value))
    if parameters:
        return parameters
    else:
        return False


def save_algorithm(alg):
    try:
        parameters = get_algorithm_parameters(alg)
        if parameters is False:
            return False
        else:
            algorithm_obj = Algorithm(*parameters)
            db.session.add(algorithm_obj)
            db.session.commit()
            return algorithm_obj.id
    except Exception:
        logging.critical(f"Got error saving Algorithm: {traceback.format_exc()}")
        return False


def save_rule(rule, alg):
    try:
        if rule.get("type") is None or rule.get("param") is None \
                or rule.get("param_value") is None and rule.get("type") != "auto":
            return False
        else:
            if rule.get("priority") is None:
                priority = 0
            else:
                priority = int(rule.get("priority"))
            rule_obj = Rule(rule["type"], priority, rule["param"], rule["param_value"], alg, rule.get("creator"))
            db.session.add(rule_obj)
            db.session.commit()
            return rule_obj.id
    except Exception:
        logging.critical(f"Got error saving Rule: {traceback.format_exc()}")
        return False


@app.route("/save_rule", methods=['GET', 'POST'])
def save_rule_and_algorithm(rule_json=None):
    if rule_json is None and request:
        rule_json = request.json
    algorithm_json = rule_json["emulate_algoritm"]
    algorithm_id = save_algorithm(algorithm_json)
    if algorithm_id is False:
        return "An error occurred when saving the Algorithm"
    else:
        rule_id = save_rule(rule_json, algorithm_id)
        if rule_id is False:
            return "An error occurred when saving the Rule"
        else:
            return f"Rule successfully saved with ID:{rule_id} and algorithm with ID:{algorithm_id}"


@app.route('/rules')
def rules():
    rules_query = Rule.query.all()
    try:
        if rules_query:
            return render_template('rules.html', rules=rules_query)
        else:
            return "No rules in the database"
    except Exception:
        logging.critical(f"Got error saving Rule: {traceback.format_exc()}")
        return f"An error occurred generating page rules (rules = {rules_query}"


@app.route('/algorithm/<int:algorithm_id>')
def algorithm(algorithm_id):
    algorithm_obj = Algorithm.query.get_or_404(algorithm_id)
    return render_template('algorithm.html', algorithm=algorithm_obj)


@app.route('/clear_rules')
def clear_rules():
    Algorithm.query.delete()
    Rule.query.delete()
    db.session.commit()
    return "Algorithms & Rules successfully cleared"


@app.route("/test_emulate", methods=['POST'])
def test_emulate():
    """
    Эмуляция посещения страницы через Selenium

    :return: Успех/Неудача посещения страницы
    """

    def check_vmc(user, value):
        """
        Проверка, был ли ранее использован пользователем указанный vmc

        :param user: проверяемый пользователь
        :param value: значение vmc

        :return: False - не был использован, True - был использован
        """
        if user.used_vmc is None:
            return False
        else:
            if value in user.used_vmc.split(","):
                return True
            else:
                return False

    def save_vmc(user, value):
        """
        Сохранение использованного при посещении страницы vmc за пользователем

        :param user: объект пользователя, которому присваивается полученный vmc
        :param value: значение vmc
        """
        if user.used_vmc is None:
            user.used_vmc = value
        else:
            user.used_vmc += f",{value}"
        db.session.commit()

    def get_keys(request_args=None):
        key = request_args.get('key')
        vmc = request_args.get('vmc')
        xcn = request_args.get('xcn')
        save_log("Emulate", "INFO", f"Got parameters: key={key}, vmc={vmc}, xcn={xcn}")
        logging.info(f"Got parameters: key={key}, vmc={vmc}, xcn={xcn}")
        if key is None or vmc is None or xcn is None:
            return None
        else:
            return {"key": key, "vmc": vmc, "xcn": xcn}

    def check_rule(request_args=None):
        if request_args is None:
            return None
        member = request_args.get('membercode')
        if member is None:
            member = 0
        member_rules = Rule.query.filter_by(creator=member).order_by(Rule.priority.desc()).all()
        if not member_rules:
            member_rules = Rule.query.filter_by(creator=0).order_by(Rule.priority.desc()).all()

        params_list = []
        for key, value in request.args.items():
            if key in ["key", "vmc", "xcn"] is False:
                param_dict = {"param_name": key, "param_value": value}
                params_list.append(param_dict)

        chosen_rule = None
        for mr in member_rules:
            for param in params_list:
                if mr.param_name == param["param_name"] and mr.param_value == param["param_value"]:
                    defined_rules = mr
                    break
            if chosen_rule is not None:
                break


    def add_rule(rule=None):
        pass

    def update_algorithm(algorithm_id=None):
        pass

    def make_visit(keys):
        user_data = UserInfo.query.filter(UserInfo.key == keys["key"]).first()
        logging.info(f"Found User: {user_data}")
        if user_data is not None:
            save_log("Emulate", "INFO", f"Found User: {user_data}")
            if check_vmc(user_data, keys["vmc"]) is False:
                visit = page_visitor.Browser().visit_page(user_data, vmc=keys["vmc"], xcn=keys["xcn"])
                if visit is True:
                    save_log("Emulate", "INFO", f"User {keys['key']} successfully visited page.")
                    save_vmc(user_data, keys["vmc"])
                    return "Page successfully visited."
                else:
                    save_log("Emulate", "ERROR", f"User {keys['key']} not visited page. (Source link: {user_data.link}")
                    return "Page not visited."
            else:
                save_log("Emulate", "ERROR",
                         f"User {keys['key']} not visited page. This vmc ({keys['vmc']}) is already used.")
                return f"Page not visited. This vmc ({keys['vmc']}) is already used."
        else:
            save_log("Emulate", "ERROR", f"Can't visit page: User not found.")
            return "User not found."

    keys_dict = get_keys(request.args)
    if keys_dict is not None:
        return make_visit(keys_dict)
    else:
        save_log("Emulate", "ERROR", "Can't visit page: required parameters are missing")
        return "Page not visited."
