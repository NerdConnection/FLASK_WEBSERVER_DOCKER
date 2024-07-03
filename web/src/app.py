from flask import Flask, url_for, redirect, render_template, request, jsonify
import docker
from post_data import posts

last_id = posts[-1]['id']
app = Flask(__name__, static_url_path='/static')
client = docker.from_env()
@app.route('/')
def home():
    return render_template("index.html")



@app.route('/container1', methods = ['POST','GET'])
def container1():
    if(request.method == "POST"):
        model_id = request.json['model_id']  # 클라이언트가 전송한 모델 ID
        try:
            # 모델 ID에 따라 적절한 Docker 이미지를 실행
            container = client.containers.run(model_id, command="python /app/test.py", detach=True)

            # 여기서 컨테이너의 IP 주소 등을 반환하여 P2P 연결에 사용할 수 있음
            
            #로그 가져오기
            logs = container.logs()
            print(logs.decode('utf-8'))

            # 컨테이너가 종료될 때까지 대기 후 정지, 삭제
            container.wait()
            container.stop()
            container.remove()
            
            
            return jsonify({'status': 'success', 'logs': logs.decode('utf-8')})
        except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
    return render_template("container1.html")










@app.route('/about_me')
def about_me():
    return "This is the about me page"

@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        subtitle = request.form['subtitle']
        content = request.form['content']
        global last_id

        last_id += 1
        new_post = {
            "id" : last_id,
            "title" : title,
            "subtitle" : subtitle,
            "content" : content
        }
        posts.append(new_post)

        with open('post_data.py', 'w') as f:
            f.write(f"posts = {posts}\n")
        f.close()
        return redirect("/")

    return render_template("create.html")

@app.route('/post/read/<int:id>')
def read(id):
    title = ''
    subtitle = ''
    content = ''
    for p in posts:
        if(p['id'] == id):
            title = p['title']
            subtitle = p['subtitle']
            content = p['content']
    return f'제목 : {title}<br/>부제목 : {subtitle}<br/>내용 : {content}<br>'    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)