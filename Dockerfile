FROM python:3.9

# Create a folder /app if it doesn't exist,
# the /app folder is the current working directory
WORKDIR /app

# Copy necessary files to our app
COPY ./app/main.py /app

COPY ./app/utils/predict_utils.py /app/utils/

COPY ./requirements.txt /app

COPY ./model/resnet50-model-augmentation.pth /app/model/

COPY ./data/test /app/data/test

# COPY ./data/train /app/data/train

# Take note port expose
EXPOSE 30000

# Disable pip cache to shrink the image size a little bit,
# since it does not need to be re-installed
RUN pip install -r requirements.txt --no-cache-dir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]