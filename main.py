import os.path
import numpy as np
import sys
import argparse
import cv2 as cv

from utils.sendImageTelegram import *


def getOutputsNames(net):

    layersNames = net.getLayerNames()

    return [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]


def drawPred(classId, conf, left, top, right, bottom):

    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    label = '%.2f' % conf

    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    labelSize, baseLine = cv.getTextSize(
        label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(
        1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top),
               cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)


def postProcess(frame, outs):

    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []

    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(classIds[i], confidences[i], left,
                 top, left + width, top + height)
        if classIds[i] == 67:
            cv.imwrite("photo.jpg", frame)
            sendImageTelegram(
                "photo.jpg", "Esta persona está usando su celular en clase")


if __name__ == "__main__":

    # Props
    confThreshold = 0.5
    nmsThreshold = 0.4
    inpWidth = 320
    inpHeight = 320

    # Arguments
    parser = argparse.ArgumentParser(
        description='Object Detection using Yolo in OpenCV')
    parser.add_argument('--image', help="Path to image file.")
    parser.add_argument('--video', help='Path to video file.')
    args = parser.parse_args()

    # Yolo classes
    classesFile = 'config/coco.names'
    classes = None
    with open(classesFile, 'rt') as r:
        classes = r.read().rstrip('\n').split('\n')

    # Model
    modelConfig = os.path.join('config', 'yolov3.cfg')
    modelWeights = os.path.join('weights', 'yolov3.weights')

    # Net
    net = cv.dnn.readNetFromDarknet(modelConfig, modelWeights)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

    # Window
    windowName = 'Deep learning object detection in OpenCV'
    cv.namedWindow(windowName, cv.WINDOW_NORMAL)

    # Output video
    outputFile = 'output_video.avi'

    # Verify arguments
    if args.image:
        if not os.path.isfile(args.image):
            print("Input image file ", args.image,  " doesn't exist")
            sys.exit(1)
        cap = cv.VideoCapture(args.image)

    elif args.video:
        if not os.path.isfile(args.video):
            print("Input video file ", args.video, " doesn't exist")

    else:
        cap = cv.VideoCapture(0)

    if not args.image:
        videoWriter = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (round(
            cap.get(cv.CAP_PROP_FRAME_WIDTH)), round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

    while cv.waitKey(1) < 0:

        hasFrame, frame = cap.read()

        if not hasFrame:
            print("Done processing !!!")
            print("Output file is stored as ", outputFile)
            cv.waitKey(3000)
            break

        blob = cv.dnn.blobFromImage(
            frame, 1/255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

        net.setInput(blob)

        outs = net.forward(getOutputsNames(net))

        postProcess(frame, outs)

        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (
            t * 1000.0 / cv.getTickFrequency())
        cv.putText(frame, label, (0, 15),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

        if (args.image):
            cv.imwrite('outputFile.jpg', frame.astype(np.uint8))
        else:
            videoWriter.write(frame.astype(np.uint8))

        cv.imshow(windowName, frame)
