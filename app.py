import os
import pickle
from flask import Flask, render_template, request, redirect, url_for

images = sorted(os.listdir("static/images"))

app = Flask("test_app", static_folder='static')





def save_user_data(user, data):
    file_name = f'labels/{user}.pkl'
    with open(file_name, 'wb') as f: 
        pickle.dump(data, f)

def load_user_data(user):
    file_name = f'labels/{user}.pkl' 
    with open(file_name, 'rb') as f:
        return pickle.load(f)


users = {}
@app.route('/', methods=['GET', 'POST'])
def index():
    

    if request.method == 'GET':
        
        for user_file in sorted(os.listdir('labels'),key=str.casefold):
            if user_file.endswith('.pkl'):
                user = user_file.split('.')[0]
                user_data = load_user_data(user)
                users[user] = {
                    'progress': user_data['progress']
                }
                


    if request.method == 'POST': 
        user_name = request.form['user_name']
        if user_name not in users:
             # Create new file
            user_data = {'progress': 0, 'labels': {}}
            save_user_data(user_name, user_data)
            users[user_name] = {'progress': 0}
            
    return render_template('index.html', users=users, total=len(images))

class_labels = ['Dog', 'Cat', 'Horse', 'Car']
confidences = [0, 0.25, 0.50, 0.75, 1.0]

@app.route('/label/<user_name>', methods=['GET', 'POST'])
def label(user_name):
    user_data = load_user_data(user_name)

    # Ensure 'progress' key exists in user_data
    if 'progress' not in user_data:
        user_data['progress'] = 0

    current = user_data['progress']

    if current >= len(images):
        return "All images labeled."

    if request.method == 'POST':
        action = request.form['action']

        if action == 'previous' and current > 0:
            current -= 1
        elif action == 'next' and current < len(images) - 1:
            current += 1

        # Save labels
        image_name = images[current]
        submitted_label = {}
        for class_label in class_labels:
            submitted_label[class_label] = request.form[class_label]

        if 'Ambiguous' in request.form:
            submitted_label['Ambiguous'] = 1
        else:
            submitted_label['Ambiguous'] = 0

        user_data['labels'][image_name] = submitted_label
        user_data['progress'] = current

        if action == 'home':
            return redirect(url_for('index'))

        save_user_data(user_name, user_data)

    # Process data for rendering
    image_name = images[current]
    labels_for_image = user_data['labels'].get(image_name, {})

    return render_template('label.html', user_name=user_name, progress=current, image=image_name,
                           class_labels=class_labels, confidences=confidences,
                           labels_for_image=labels_for_image, total=len(images))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
