from config_path import data
def index():
    fp=open(data.path+"/project_data/ok.html","r");
    dt=fp.read()
    return """<html>%s</html>"""%(dt)
