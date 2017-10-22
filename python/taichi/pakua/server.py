from flask import Flask, render_template, send_from_directory, send_file, request
from taichi.misc.settings import get_output_directory
import os
from taichi import get_output_directory
from flask_cors import CORS
import json
import base64

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
#CORS(app)


@app.route('/viewer/<path:path>')
def send_front_end_file(path):
  return send_from_directory('viewer', path)

@app.route('/data', methods=['POST'])
def next_frame():
  content = request.get_json(silent=True)
  print(content)
  directory = os.path.join(get_output_directory(), content['path'])
  files = sorted(os.listdir(directory))
  files = list(filter(lambda x: x.endswith('.json'), files))
  frame_fn = '%04d.json' % content['frame_id']
  next_frame = files[(files.index(frame_fn) + content['inc']) % len(files)].split('.')[0]
  next_frame = int(next_frame)
  
  json_path = os.path.join(directory, frame_fn)
  response = {
    'next_frame': next_frame
  }
  if content['need_geometry']:
    with open(json_path) as f:
      response['data'] = json.loads(f.read())
  return json.dumps(response)


@app.route('/')
def browse_outputs():
  output_dir = get_output_directory()
  dirs = os.listdir(output_dir)
  dirs = sorted(dirs)
  entries = []
  for d in dirs:
    entries.append({
        'title': d,
        'text': '',
    })
  return render_template('browser.html', entries=entries)


@app.route('/view/<folder>')
def view(folder):
  output_dir = get_output_directory()
  return render_template('view.html', folder=folder)

frame_buffer = os.path.join(get_output_directory(), 'frame_buffer')

@app.route('/clear_frame_buffer', methods=['POST'])
def clear_frame_buffer():
  try:
    os.mkdir(frame_buffer):
  except Exception as e:
    print(e)
  os.li
  return ''

@app.route('/make_video', methods=['POST'])
def make_video():
  return ''

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
  img = str(request.data).split(',')[1]
  img = base64.decodebytes(img.encode())
  #with open('a.png', 'wb') as f:
  #  f.write(img)
  return ''
    
def get_pakua_server():
  return app
