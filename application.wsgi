#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import __main__
__main__.__requires__ = ['jinja2 >= 2.4']
import pkg_resources

from flask import Flask
application = Flask(__name__)
application.secret_key = 'some_secret'
from flask import request
from flask import abort
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for

import os
from werkzeug import secure_filename
import tempfile
import subprocess
import posixpath
import shutil

import satellite_sanity

UPLOAD_FOLDER = '/tmp/satellite-sanity'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
FILES = ['sosreport', 'spacewalk-debug', 'satellite-sanity']

def extract(filename, directory):
    cwd = os.getcwd()
    os.makedirs(directory)
    os.chdir(directory)
    # Various extraction commands for various file extensions
    if filename.endswith('.tar'):
        command = ['tar', '-xf', filename, '--strip', '1', '--no-same-permissions', '--no-same-owner']
    elif filename.endswith('.tar.gz'):
        command = ['tar', '-xzf', filename, '--strip', '1', '--no-same-permissions', '--no-same-owner']
    elif filename.endswith('.tar.bz2'):
        command = ['tar', '-xjf', filename, '--strip', '1', '--no-same-permissions', '--no-same-owner']
    elif filename.endswith('.tar.xz'):
        command = ['tar', '-xJf', filename, '--strip', '1', '--no-same-permissions', '--no-same-owner']
    else:
        raise Exception("Unknown archive extension %s" % filename)
    # Extract
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Ensure there was no content in stderr
    stdout, stderr = process.communicate()
    assert len(stderr) == 0, "Extraction failed with '%s' when running '%s'" % (stderr, command)
    os.chdir(cwd)

def du(start_path):
    """http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        if not os.access(dirpath, os.X_OK):
            continue
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

@application.route("/", methods=['GET', 'POST'])
@application.route("/<directory_relative>", methods=['GET', 'POST'])
def index(directory_relative=None):
    uploaded = {}
    if request.method == 'POST':
        for f in FILES:
            ff = request.files[f]
            if ff:
                filename = secure_filename(ff.filename)
                filename = os.path.join(application.config['UPLOAD_FOLDER'], filename)
                ff.save(filename)
                uploaded[f] = filename
                flash("File %s uploaded as %s" % (f, filename))
        if uploaded:
            directory = tempfile.mkdtemp(suffix='', prefix='web', dir=application.config['UPLOAD_FOLDER'])
            for f, filename in uploaded.iteritems():
                extracted = os.path.join(directory, f)
                extract(filename, extracted)
                flash("File %s (%s) extracted to %s" % (f, filename, extracted))
        return redirect(url_for('index', directory_relative=os.path.basename(directory)))
    elif request.method == 'GET':
        if directory_relative:
            directory_relative = secure_filename(directory_relative)
            directory = os.path.join(application.config['UPLOAD_FOLDER'], directory_relative)
            rules = satellite_sanity.plugins.rules()
            data = satellite_sanity.input_data.InputData(directory)
            results = rules.run(['Satellite_5', 'general'], [], data)
            return render_template('index.html', directory_relative=directory_relative, results=results)
        else:
            dirs = {}
            for i in os.listdir(application.config['UPLOAD_FOLDER']):
              ii = os.path.join(application.config['UPLOAD_FOLDER'], i)
              if os.path.isdir(ii):
                dirs[i] = du(ii)
            return render_template('index.html', files=FILES, dirs=dirs)

@application.route("/file/<directory_relative>/<path:data_file>", methods=['GET'])
def file(directory_relative, data_file):
    directory_relative = secure_filename(directory_relative)
    name = os.path.join(application.config['UPLOAD_FOLDER'], directory_relative, data_file)
    name = posixpath.normpath(name)
    if not name.startswith(application.config['UPLOAD_FOLDER']):
        abort("Unexpected file name")
    fp = open(name, 'r')
    filecontent = fp.readlines()
    fp.close()
    return render_template('index.html', filecontent=filecontent)

@application.route("/delete/<directory_relative>", methods=['GET'])
def delete(directory_relative):
    directory_relative = secure_filename(directory_relative)
    directory = os.path.join(application.config['UPLOAD_FOLDER'], directory_relative)
    shutil.rmtree(directory)
    flash("Directory '%s' removed" % directory)
    return redirect(url_for('index'))

if __name__ == '__main__':
    application.debug = True
    application.run()
