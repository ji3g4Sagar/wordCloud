from flask import render_template, request, send_from_directory, jsonify
from app import app
import os
from app.VoiceAPIClass import voiceAnalysis
import urllib.request

app.config['JSON_AS_ASCII'] = False

@app.route('/')
@app.route('/index')
def index():
    return render_template("123.html")


@app.route('/getfile', methods=['get'])
def getfile():
    filename = request.args.get('filename')
    os.chdir("/home/visteam/www/yuan/voiceapi/speech_voice") 
    return send_from_directory(os.getcwd(), filename, as_attachment=True)

@app.route('/analysis', methods=['get'])
def analysis():
	# file will store in local directory which name "downloadvoic"
	fileName = request.args.get('filename')
	url = "http://140.138.77.90:6667/getfile?filename=" + fileName
	localStoreDirectory = "/home/visteam/www/yuan/voiceapi/downloadvoice/" + fileName
	print(localStoreDirectory)
	urllib.request.urlretrieve(url, localStoreDirectory)
	analysis = voiceAnalysis()
	resultString = ""
	resultdic = ""
	resultdic = analysis.analysisVoice(fileName)
	#print(resultdic)
	#for sep in resultdic:
	#    resultString = resultString+ sep
	#return resultString
	#return (analysis.analysisVoice(fileName))
	return jsonify(resultdic)


@app.route('/cloud', methods=['get'])
def cloud():
    return render_template("trycloud4.html")
