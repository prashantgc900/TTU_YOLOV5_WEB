from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, flash
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
from datetime import datetime
import zipfile
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

app.secret_key = "pgc@METIS"

today = datetime.now()
folder_name = today.strftime("%b-%d-%Y-%H-%M-%S")
uploads_dir = os.path.join(app.instance_path, 'uploads', folder_name)


os.makedirs(uploads_dir, exist_ok=True)


def createzip():
    examplezip = zipfile.ZipFile(
        'static/'+folder_name+'/labels/labels.zip', 'w')
    for x in os.listdir('static/'+folder_name+'/labels/'):
        examplezip.write('static/'+folder_name+'/labels/'+x,
                         compress_type=zipfile.ZIP_DEFLATED)
    examplezip.close()


def labels(path):
    glue = []
    broken = []
    foobar = []
    one_wire = []
    two_wire = []
    all_wire = []
    good = []

    for x in os.listdir(path):
        image_name = x.replace(".txt", ".jpg")
        file1 = open(path+x, 'r')
        Lines = file1.readlines()
        category = [int(line.strip()[0]) for line in Lines]
        if(1 not in category and 2 not in category and 3 not in category):
            good.append(image_name)
        else:
            if 1 in category:
                broken.append(image_name)
            if 2 in category:
                glue.append(image_name)
            if 3 in category:
                foobar.append(image_name)
        if category.count(0) == 1:
            one_wire.append(image_name)
        elif category.count(0) == 2:
            two_wire.append(image_name)
        elif category.count(0) == 3:
            all_wire.append(image_name)
    return glue, broken, foobar, one_wire, two_wire, all_wire, good


def create_hist(module3, module4, module5, module6, current_model):
    plt.figure(figsize=(15, 6))
    X = ['Glue', 'Broken', 'FooBar', 'One Third',
         'Two Third', 'All Wires', 'Good']
    w = 0.17
    bar1 = np.arange(len(X))
    bar2 = [i+w for i in bar1]
    bar3 = [i+w for i in bar2]
    bar4 = [i+w for i in bar3]
    bar5 = [i+w for i in bar4]

    plt.xticks(bar3, X)
    plt.xlabel("Class", fontsize=12,labelpad=15)
    plt.ylabel("Number", fontsize=12,labelpad=15)

    plt.bar(bar1, module3, w, label='Module3')
    plt.bar(bar2, module4, w, label='Module4')
    plt.bar(bar3, module5, w, label='Module5')
    plt.bar(bar4, module6, w, label='Module6')
    plt.bar(bar5, current_model, w, label='Current Module')
    plt.legend()
    plt.savefig('static/Histogram.png', dpi=100)


@app.route("/")
def uploader():
    global today
    global folder_name
    global uploads_dir
    if folder_name in os.listdir('static/'):
        print("Inside Loop")
        path = 'static/'+folder_name
        # Sorting as per image upload date and time
        uploads = sorted(os.listdir(path))
        # uploads = os.listdir('static/uploads')
        uploads = [folder_name+"/" + file for file in uploads]
        gluelist, brokenlist, foobarlist, one_wirelist, two_wirelist, all_wirelist, goodlist = labels(
            'static/'+folder_name+'/labels/')
        gluelist3, brokenlist3, foobarlist3, one_wirelist3, two_wirelist3, all_wirelist3, goodlist3 = labels(
            'database/Module3/labels/')
        gluelist4, brokenlist4, foobarlist4, one_wirelist4, two_wirelist4, all_wirelist4, goodlist4 = labels(
            'database/Module4/labels/')
        gluelist5, brokenlist5, foobarlist5, one_wirelist5, two_wirelist5, all_wirelist5, goodlist5 = labels(
            'database/Module5/labels/')
        gluelist6, brokenlist6, foobarlist6, one_wirelist6, two_wirelist6, all_wirelist6, goodlist6 = labels(
            'database/Module6/labels/')
        glue = [folder_name+"/" + file for file in gluelist]
        broken = [folder_name+"/" + file for file in brokenlist]
        foobar = [folder_name+"/" + file for file in foobarlist]
        one_wire = [folder_name+"/" + file for file in one_wirelist]
        two_wire = [folder_name+"/" + file for file in two_wirelist]
        all_wire = [folder_name+"/" + file for file in all_wirelist]
        good = [folder_name+"/" + file for file in goodlist]
        labelnames = [folder_name+"/labels/labels.zip"]
        module3 = [len(gluelist3), len(brokenlist3), len(foobarlist3), len(
            one_wirelist3), len(two_wirelist3), len(all_wirelist3), len(goodlist3)]
        module4 = [len(gluelist4), len(brokenlist4), len(foobarlist4), len(
            one_wirelist4), len(two_wirelist4), len(all_wirelist4), len(goodlist4)]
        module5 = [len(gluelist5), len(brokenlist5), len(foobarlist5), len(
            one_wirelist5), len(two_wirelist5), len(all_wirelist5), len(goodlist5)]
        module6 = [len(gluelist6), len(brokenlist6), len(foobarlist6), len(
            one_wirelist6), len(two_wirelist6), len(all_wirelist6), len(goodlist6)]
        current_module = [len(gluelist), len(brokenlist), len(foobarlist), len(
            one_wirelist), len(two_wirelist), len(all_wirelist), len(goodlist)]
        create_hist(module3, module4, module5, module6, current_module)
        createzip()
        
        today = datetime.now()
        folder_name = today.strftime("%b-%d-%Y-%H-%M-%S")
        uploads_dir = os.path.join(app.instance_path, 'uploads', folder_name)
        
        
        os.makedirs(uploads_dir, exist_ok=True)

        return render_template("index.html", uploads=uploads, glue=glue, broken=broken, foobar=foobar,
                               one_wire=one_wire, two_wire=two_wire, all_wire=all_wire, good=good, labelnames=labelnames, gluelist=gluelist, brokenlist=brokenlist, foobarlist=foobarlist, one_wirelist=one_wirelist, two_wirelist=two_wirelist, all_wirelist=all_wirelist, goodlist=goodlist)
    else:
        return render_template('index.html')


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        files = request.files.getlist('files[]')
        print(files)
        for f in files:
            filename = secure_filename(f.filename)
            f.save(os.path.join(uploads_dir, filename))
            print(filename)
        flash('File(s) successfully uploaded')
    return detect()


@app.route("/detect")
def detect():
    subprocess.run("ls")
    print(uploads_dir)
    subprocess.run(['python3', 'detect.py', '--weights', 'updated.pt', '--source', uploads_dir, '--img', '640',
                   '--conf', '0.5', '--project', 'static', '--name', folder_name, '--save-txt','--device','0'])
    return redirect("/")


@app.route('/return-files', methods=['GET'])
def return_file():
    # obj = request.args.get('obj')
    # f=(os.listdir("runs/detect/"))[-1]
    # print(f)
    # loc = os.path.join("runs/detect/"+f, obj)
    # print(loc)
    folder = (os.listdir("runs/detect/"))[-1]
    filename = (os.listdir("runs/detect/"+f+"/"))[-1]
    path = "runs/detect/"+folder+"/"+filename
    try:
        return send_file(path)
        # return send_from_directory(loc, obj)
    except Exception as e:
        return str(e)

# @app.route('/display/<filename>')
# def display_video(filename):
# 	#print('display_video filename: ' + filename)
# 	return redirect(url_for('static/video_1.mp4', code=200))
