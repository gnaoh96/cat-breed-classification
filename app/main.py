import io
import os

import numpy as np
import torch
from fastapi import FastAPI, File, UploadFile
from loguru import logger
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from PIL import Image
from utils.predict_utils import define_device, load_model, transform_img

os.environ["CUDA_LAUNCH_BLOCKING"] = "0"

# Save all files and result to cached
# by a dictionary with key is image hash
# cache = {}

# Create a tracer provider and set the exporter
set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "cbp-service"}))
)
tracer = get_tracer_provider().get_tracer("mycbp", "0.0.1")

# Configure the Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAEGER_HOST", "localhost"),
    agent_port=os.getenv("JAEGER_PORT", "6831"),
)
span_processor = BatchSpanProcessor(jaeger_exporter)
get_tracer_provider().add_span_processor(span_processor)

# Initialize app with FastAPI()
app = FastAPI()

# Instrument the FastAPI app
FastAPIInstrumentor().instrument_app(app)


@app.post("/cat-breed-prediction")
def cat(file: UploadFile = File(...)):
    predict_image = None

    logger.info("Try to verify and open image")
    try:
        file.verify()  # verify img is an image (not string of path)
        predict_image = Image.open(file.file)
    except Exception:
        predict_image = Image.open(file.file)

    device = define_device()
    image_transforms, augmented_image_transforms, idx_to_class = transform_img()
    model = load_model(device)
    k = 3

    # open and transform the image
    transform = augmented_image_transforms["test"]

    predict_image_tensor = transform(predict_image)
    predict_image_tensor = predict_image_tensor.view(1, 3, 224, 224)
    predict_image_tensor = predict_image_tensor.to(device)

    # output = io.StringIO()

    logger.info("Predicting. Please wait...")

    result = {"Top": [], "Breed": [], "Ratio": []}

    try:
        with torch.no_grad():
            model.eval()
            out = model(predict_image_tensor)
            ps = torch.exp(out)

            # get the topk result
            topprob, topclass = ps.topk(k, dim=1)
            topprob_np = topprob.cpu().numpy()[0]
            topclass_np = topclass.cpu().numpy()[0]

            # print the prediction result
            print("Top", k, "prediction :")
            for idx, prob in enumerate(topprob_np):
                # print(
                #     "-",
                #     "Top:",
                #     (idx + 1),
                #     idx_to_class[topclass_np[idx]],
                #     ":",
                #     f"{prob*100:.2f}% ",
                #     file=output,
                # )
                top = idx + 1
                breed = idx_to_class[topclass_np[idx]]
                ratio = f"{prob*100:.2f}%"

                result["Top"].append(top)
                result["Breed"].append(breed)
                result["Ratio"].append(ratio)

        # Store output's result
        # result = output.getvalue()
        logger.info("Predict successfully")
    except Exception as e:
        logger.info("Predict un-successfully")
        print("Error:", e)

    # cache[pil_hash] = result
    return result
