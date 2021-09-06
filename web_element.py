from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


def web_element(d, name, elements=False, class_name=False, tag_name=False, xpath=False, send_keys=False, attribute="",
                index=-2):
    if not class_name and not tag_name and not xpath:
        print("Idiot")

    fun_name = f"find_element_by_"
    if elements:
        fun_name = fun_name.replace("element", "elements")
    if class_name:
        fun_name += "class_name"
    elif tag_name:
        fun_name += "tag_name"
    elif xpath:
        fun_name += "xpath"
    web_ele = getattr(d, fun_name)(name)

    if attribute:
        if index != -2:
            return web_ele[index].get_attribute(attribute)
        else:
            return web_ele.get_attribute(attribute)
    if send_keys:
        web_ele.send_keys(send_keys)
        return

    return web_ele


def click_on_element(d, element):
    if isinstance(element, str):
        if web_element(d, element, class_name=True, elements=True):
            ele = web_element(d, element, class_name=True)
        else:
            raise ValueError
    else:
        ele = element

    with ActionChains(d) as a:
        a.click(ele)
        a.perform()


def element_exsist(d, ele):
    try:
        web_element(d, ele, class_name=True)
    except NoSuchElementException:
        return False
    return True
