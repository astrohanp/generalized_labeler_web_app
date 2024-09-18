# Image Labeling App

This is an image labeling application developed to streamline the process of labeling data for training classifiers. Initially created during my time at **Schlumberger Doll-Research Center**, the primary motivation was the lack of straightforward tools for manually labeling images while keeping the data private. I designed this app to address that need, and I hope it can be useful to others facing similar challenges.

## Key Features:
- **Private and Secure**: You can run this app on your local server, ensuring that your data remains private and secure.
- **Customizable Labeling Interface**: The app allows you to easily label images with predefined classes and confidence levels using an intuitive user interface.
- **Progress Tracking**: Your progress is saved automatically, and you can resume labeling at any time.
- **Ambiguity Handling**: You can mark images as ambiguous if you're uncertain, and easily adjust class probabilities based on confidence.
- **Responsive Design**: The app is designed to be user-friendly and works on various screen sizes.

## Additional Benefits:
- **Customizable Labels**: Easily modify the classes or confidence levels to suit your specific needs.
- **Ambiguity Management**: Handle ambiguous cases directly within the interface with the "Ambiguous" checkbox for uncertainty.
- **Easy Deployment**: Run the app locally, ensuring data security.
- **Sample Data**: The `static/images` folder includes sample data for testing the application.

## Getting Started

### Prerequisites:
- Python 3.x
- Flask
- Apache server with **mod_wsgi**

### Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/image-labeling-app.git
   cd image-labeling-app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Apache to serve the Flask app using **mod_wsgi**.

### Apache Setup with mod_wsgi:
1. **Install mod_wsgi**:
   On Ubuntu, install the required package:
   ```bash
   sudo apt-get install libapache2-mod-wsgi-py3
   ```

2. **Create a WSGI entry point** for the app:
   Create a file named `image_labeler_app.wsgi` in the app's root directory with the following content:
   ```python
   import sys
   import logging
   from app import app as application

   logging.basicConfig(stream=sys.stderr)
   sys.path.insert(0, "/path/to/image-labeling-app")
   ```

3. **Configure Apache**:
   Open your Apache configuration file (usually located at `/etc/apache2/sites-available/000-default.conf` or `/etc/apache2/sites-available/your-site.conf`) and add the following configuration:
   ```apache
   <VirtualHost *:80>
       ServerName your-domain.com
       WSGIDaemonProcess image_labeler_app threads=5
       WSGIScriptAlias / /path/to/image-labeling-app/image_labeler_app.wsgi

       <Directory /path/to/image-labeling-app>
           Require all granted
       </Directory>

       Alias /static /path/to/image-labeling-app/static
       <Directory /path/to/image-labeling-app/static/>
           Require all granted
       </Directory>

       ErrorLog ${APACHE_LOG_DIR}/error.log
       CustomLog ${APACHE_LOG_DIR}/access.log combined
   </VirtualHost>
   ```

4. **Enable mod_wsgi** and restart Apache:
   ```bash
   sudo a2enmod wsgi
   sudo systemctl restart apache2
   ```

Now, your app should be available at `http://your-domain.com`, and other users can access it via the web browser to label data.

### Usage:
1. Enter your name and start labeling the images.
2. Assign confidence levels to each class using the radio buttons.
3. Mark ambiguous images with the checkbox if necessary.
4. Your progress will be automatically saved, and you can resume anytime.

## Running with Docker

You can also run the application inside a Docker container for easier deployment and management. Below are the steps for building and running the app in both **debug** and **deployment** modes using Docker.

### Build the Docker Image:
First, build the Docker image for the application:
```bash
sudo docker build . -t image_labeler_web_app
```

### Run in Debug Mode:
To run the application in debug mode, which allows you to enter the container interactively:
```bash
sudo docker run -it -p 5000:5000 \
-v /path/to/labels:/IMAGE_LABELER_WEB_APP/labels \
-v /path/to/static/images:/IMAGE_LABELER_WEB_APP/static/images \
image_labeler_web_app /bin/bash
```
This mounts your `labels` and `static/images` directories into the container and opens an interactive shell.

### Run in Deployment Mode:
To run the application in the background (deployment mode), use the following command:
```bash
sudo docker run -d -p 5000:5000 \
-v /path/to/labels:/IMAGE_LABELER_WEB_APP/labels \
-v /path/to/static/images:/IMAGE_LABELER_WEB_APP/static/images \
image_labeler_web_app
```

### Debugging the Container:
1. To enter the container:
   ```bash
   docker exec -it CONTAINER_ID /bin/sh
   ```
   
2. To view logs from the last hour:
   ```bash
   docker logs -t --since 1h CONTAINER_ID
   ```

3. To view and follow logs from the last hour:
   ```bash
   docker logs -f -t --since 1h CONTAINER_ID
   ```

## Folder Structure:
- `app.py`: Contains the Flask app code.
- `templates/index.html`: Main page where users input their name and start/resume labeling.
- `templates/label.html`: Page where images are displayed, and users assign labels.
- `static/images/`: Contains sample images for labeling.

## License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments:
Special thanks to the team at Schlumberger Doll-Research Center for their support during the development of this tool.